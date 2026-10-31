import importlib.util
import json
import pkgutil

import pygame as pg
from termcolor import colored

import entity.concrete as ec
import terrain.concrete as tc
from entity import entity_registry
from event_handler.event_handler import Event
from event_handler.events import Events
from run_modes import RunModes
from terrain import terrain_registry


class Engine:
    _instance = None

    def __init__(self, run_mode):
        if Engine._instance is not None:
            raise RuntimeError("Engine already exists - use Engine.get_instance() instead")

        self.screen = None
        self.clock = None
        self.running = False
        self.run_mode = run_mode
        self.editing_mode = False
        self.registries = {}

        Engine._instance = self

    def init(self):
        import os
        import pygame as pg
        import src.config as c
        from datatype.coordinate import Coordinate
        from level.camera import Camera
        from level.dt import Dt
        from level.level import Level
        from _devtools.level_editor.overlay.editing_menu.terrain_pick_controller import TerrainPickController

        pg.init()
        os.system('color')

        self.screen = pg.display.set_mode((c.WIDTH, c.HEIGHT))
        Camera(Coordinate(c.ROOM_WIDTH // 2, c.HEIGHT // 2))
        Level()
        Dt()
        if self.run_mode == RunModes.EDITOR:
            TerrainPickController()
        self.clock = pg.time.Clock()
        pg.display.set_caption(c.CAPTION_EDITOR if self.run_mode == RunModes.EDITOR else c.CAPTION_DEFAULT)
        self.running = True

        #import all gameobjects to add to registry
        self.import_all_submodules(tc)
        self.import_all_submodules(ec)
        self.registries = terrain_registry.get_all() | entity_registry.get_all()

    @staticmethod
    def import_all_submodules(package):
        if isinstance(package, str):
            package = importlib.import_module(package)

        for _, name, _ in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            importlib.import_module(name)

    @staticmethod
    def update_entity():
        from level.level import Level

        level = Level.get_instance()

        for entity in level.get_layer_entity():
            entity.update()

    @staticmethod
    def update_level_entity():
        from level.level import Level

        level = Level.get_instance()

        for level_entity in level.get_layer_level_entity():
            level_entity.update()

    @staticmethod
    def update_overlay():
        from level.level import Level

        level = Level.get_instance()

        for obj in level.get_layer_overlay():
            obj.update()

    @staticmethod
    def render_overlay():
        from level.level import Level

        level = Level.get_instance()

        level.s_layer_overlay.fill((0, 0, 0, 0))
        for obj in level.get_layer_overlay():
            obj.render(level.s_layer_overlay)

    def draw(self):
        from level.level import Level

        level = Level.get_instance()
        self.screen.fill("white")

        for layer in (level.get_layer_background(),
                      level.get_layer_level(),
                      level.get_layer_level_entity(),
                      level.get_layer_entity()):
            for obj in layer:
                obj.render(self.screen)

        self.screen.blit(level.s_layer_overlay, (0, 0))

    @staticmethod
    @Event.listener(Events.ZOOM_CHANGE, Event.When.AFTER)
    def zoom_changed(cam, zoom):
        from level.level import Level
        level = Level.get_instance()
        for layer in (level.get_layer_background(), level.get_layer_level(),
                      level.get_layer_level_entity(), level.get_layer_entity()):
            for obj in layer:
                obj.create_image()

    @staticmethod
    def key_mod_down(key):
        if pg.key.get_mods() & key:
            return True
        return False

    @staticmethod
    def create_rooms_namespace():
        return ""

    @staticmethod
    def export_room():
        import os
        from terrain.level_object import EncodeLevelObject
        from level.level import Level

        id_file = 0
        name_file = "room"
        path_file = "assets/rooms/export/"

        while os.path.isfile(path_file + name_file + "_" + str(id_file) + ".json"):
            id_file += 1

        with open(path_file + name_file + '_' + str(id_file) + '.json', 'w', encoding='utf-8') as f:
            data = json.dumps({'layer_background': Level.get_instance().get_layer_background(),
                               'layer_level': Level.get_instance().get_layer_level(),
                               'layer_level_entity': Level.get_instance().get_layer_level_entity(),
                               'layer_entity': Level.get_instance().get_layer_entity_playerless()},
                              sort_keys=True, indent=4, cls=EncodeLevelObject)
            print(f"Exported room as {name_file}_{str(id_file)}.json")
            f.write(data)
            f.close()

    @staticmethod
    @Event.trigger(Events.ROOM_LOADED)
    def import_room(name, namespace=None):
        from level.level import Level

        level = Level.get_instance()

        if namespace is None:
            namespace = Engine.create_rooms_namespace()
        try:
            with open("assets/rooms/" + namespace + name + '.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                layer_bg = data["layer_background"]
                layer_level = data["layer_level"]
                layer_level_entity = data["layer_level_entity"]
                layer_entity = data["layer_entity"]

                level.cleanse_level()
                level.cleanse_level_entity()
                level.cleanse_background()
                level.cleanse_entity_playerless()

                for obj in layer_bg:
                    o = Engine.get_instance().create_import_obj(obj)
                    if o is not None:
                        level.add_background(o)
                for obj in layer_level:
                    o = Engine.get_instance().create_import_obj(obj)
                    if o is not None:
                        level.add_level(o)
                for obj in layer_level_entity:
                    o = Engine.get_instance().create_import_obj(obj)
                    if o is not None:
                        level.add_level_entity(o)
                for obj in layer_entity:
                    o = Engine.get_instance().create_import_obj(obj)
                    if o is not None:
                        level.add_entity(o)

                f.close()
        except FileNotFoundError:
            print(colored(f"Could not find room file: assets/rooms/{namespace}{name}.json"))

    @staticmethod
    def create_import_obj(obj):
        from datatype.coordinate import Coordinate

        try:
            match obj["type"]:
                case "RoomTransition":
                    o = Engine.load_class(obj["type"])(Coordinate(obj["pos"][0], obj["pos"][1]), obj["target_room"], obj["target_transition_id"], obj["transition_id"], obj["scaler"], obj["rot"])
                case "PlayerSpawner":
                    o = Engine.load_class(obj["type"])(Coordinate(obj["pos"][0], obj["pos"][1]), obj["spawner_id"], obj["scaler"], obj["rot"])
                case _:
                    o = Engine.load_class(obj["type"])(Coordinate(obj["pos"][0], obj["pos"][1]), obj["scaler"], obj["rot"])
            try:
                o.change_size(obj["size"])
            except KeyError:
                pass

            return o
        except KeyError:
            print(colored(f"Cannot load object {obj["type"]}", "red"))

    @staticmethod
    def load_class(name):
        reg = Engine.get_instance().registries
        c, _ = reg[name]
        return c

    @staticmethod
    def create_obj_files_root():
        return "src/level_objects_concrete"

    @staticmethod
    def is_file_py(name):
        return name[-3:] == ".py"

    @classmethod
    def get_instance(cls):
        return cls._instance
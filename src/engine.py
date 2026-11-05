import importlib.util
import json
import pkgutil
from enum import Enum, auto

import config as c
import pygame as pg
from termcolor import colored

import entity.concrete as ec
import terrain.concrete as tc
from entity import entity_registry
from event_handler.event_handler import Event
from event_handler.events import Events
from overlay.sided_screen_object import SidedScreenObject
from run_modes import RunModes
from terrain import terrain_registry
from utils.singleton import Singleton

class CamMode(Enum):
    FULL = auto()
    SPLIT = auto()

class Engine(metaclass=Singleton):
    def __init__(self):
        self.screens = {}
        self.clock = None
        self.running = False
        self.activated_once = False
        self.run_mode = RunModes.DEFAULT
        self.controllers = []
        self.players = {}
        self.cams = {}
        self.cam_mode = CamMode.FULL
        self.registries = {}

        Engine._instance = self

    # noinspection PyShadowingNames
    def init(self):
        import os
        import pygame as pg
        from datatype.coordinate import Coordinate
        from level.camera import Camera
        from level.dt import Dt
        from level.level import Level
        from overlay.overlays.titlescreen_menu import TitlescreenMenu
        from datatype.coordinate_screen import CoordinateScreen


        pg.init()
        os.system('color')

        self.screens["full"] = pg.display.set_mode((c.WIDTH, c.HEIGHT))
        self.screens["full"].fill((0, 0, 0))
        self.cams["full"] = Camera(Coordinate(c.WIDTH // 2, c.HEIGHT // 2), (c.WIDTH, c.HEIGHT))
        Level()
        Dt()
        self.clock = pg.time.Clock()
        pg.display.set_caption(c.CAPTION_DEFAULT)
        self.running = True

        Level.inst().add_overlay(TitlescreenMenu(CoordinateScreen(0, 0)))

    def activate_game(self, gamemode, room):
        from _devtools.level_editor.overlay.controllers.terrain_pick_controller import TerrainPickController
        from _devtools.level_editor.overlay.gui.editing_gui_menu import EditingGuiMenu
        from datatype.coordinate_screen import CoordinateScreen
        from _devtools.level_editor.overlay.gui.hacker_gui_menu import HackerGuiMenu
        from overlay.overlays.default_gui_menu import DefaultGuiMenu
        from datatype.coordinate import Coordinate
        from level.level import Level
        from player.player_big import PlayerBig
        from player.player_small import PlayerSmall
        from level.camera import Camera


        Level.inst().clear_level()
        self.run_mode = gamemode

        # create screens
        self.screens["left"] = pg.Surface((c.WIDTH / 2, c.HEIGHT)).convert()
        self.screens["right"] = pg.Surface((c.WIDTH / 2, c.HEIGHT)).convert()

        # spawn Players
        self.players["big"] = PlayerBig(Coordinate(0, 0))
        Level.inst().add_entity(self.players["big"])
        self.players["small"] = PlayerSmall(Coordinate(0, 0))
        Level.inst().add_entity(self.players["small"])

        # spawn Cams
        self.cams["big"] = Camera(self.players["big"].pos, (c.WIDTH / 2, c.HEIGHT))
        self.cams["small"] = Camera(self.players["small"].pos, (c.WIDTH / 2, c.HEIGHT))
        self.cam_mode = CamMode.SPLIT

        if not self.activated_once:
            if self.run_mode == RunModes.EDITOR:
                self.controllers.append(TerrainPickController())

            # import all gameobjects to add to registry
            self.import_all_submodules(tc)
            self.import_all_submodules(ec)
            self.registries = terrain_registry.get_all() | entity_registry.get_all()

        # Set Gui based on Gamemode
        if self.run_mode == RunModes.EDITOR:
            Level.inst().add_overlay(EditingGuiMenu(CoordinateScreen(0, 0)))
        if self.run_mode == RunModes.HACKS:
            Level.inst().add_overlay(HackerGuiMenu(CoordinateScreen(0, 0)))
        if self.run_mode == RunModes.DEFAULT:
            Level.inst().add_overlay(DefaultGuiMenu(CoordinateScreen(0, 0)))

        # load Room
        Engine.import_room(room)

        # set player pos
        try:
            self.players["big"].change_pos(Level.inst().get_player_spawner(0)[0].get_player_spawn_pos())
            self.players["small"].change_pos(Level.inst().get_player_spawner(1)[0].get_player_spawn_pos())
        except IndexError:
            print(colored("Could not find player spawner", "red"))
            self.players["big"].change_pos(Coordinate(0, 0))
            self.players["small"].change_pos(Coordinate(0, 0))

    def deactivate_game(self):
        pass

    @staticmethod
    def import_all_submodules(package):
        if isinstance(package, str):
            package = importlib.import_module(package)

        for _, name, _ in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            importlib.import_module(name)

    @staticmethod
    def update_controllers():
        for cont in Engine.inst().controllers:
            cont.update()

    @staticmethod
    def update_entity():
        from level.level import Level

        for entity in Level.inst().layer_entity:
            entity.update()

    @staticmethod
    def update_terrain():
        from level.level import Level

        level = Level.inst()

        for terrain in level.layer_level:
            terrain.update()

    @staticmethod
    def update_overlay():
        from level.level import Level

        level = Level.inst()

        for obj in level.layer_overlay:
            obj.update()

    @staticmethod
    def render_overlay_full():
        from level.level import Level

        level = Level.inst()
        full = [obj for obj in level.get_layer_overlay() if not isinstance(obj, SidedScreenObject)]
        for obj in full:
            obj.render(Engine.inst().screens["full"], Engine.inst().cams["full"])

    @staticmethod
    def render_overlay_sided():
        from level.level import Level

        level = Level.inst()
        sided = [obj for obj in level.get_layer_overlay() if isinstance(obj, SidedScreenObject)]

        for obj in sided:
            match obj.side:
                case "left":
                    side = "left"
                    cam = "big"
                case "right":
                    side = "right"
                    cam = "big"
                case _:
                    side = "none found"
                    cam = "full"
            obj.render(Engine.inst().screens[side], Engine.inst().cams[cam])

    @staticmethod
    def draw(type):
        from level.level import Level
        from level.camera import Camera

        level = Level.inst()
        screen = Engine.inst().screens[type]
        screen.fill("white")
        zoom = Camera.zoom()
        match type:
            case "left":
                cam_name = "big"
            case "right":
                cam_name = "small"
            case _:
                cam_name = "full"
        cam = Engine.inst().cams[cam_name]

        for layer in (level.get_layer_background(),
                      level.get_layer_level(),
                      level.get_layer_entity()):
            for obj in layer:
                obj.render(screen, cam, zoom)

    def render_sided(self):
        screen = self.screens["full"]
        if self.cam_mode == CamMode.SPLIT:
            screen.blit(self.screens["left"], (0, 0))
            screen.blit(self.screens["right"], (c.WIDTH / 2, 0))

    @staticmethod
    @Event.listener(Events.ZOOM_CHANGE, Event.When.AFTER)
    def zoom_changed(_, __):
        from level.level import Level
        level = Level.inst()
        for layer in (level.layer_background, level.layer_level,
                      level.layer_entity):
            for obj in layer:
                obj.create_image()

    @staticmethod
    def key_mod_down(key):
        if pg.key.get_mods() & key:
            return True
        return False

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
            data = json.dumps({'layer_background': Level.inst().get_layer_background(),
                               'layer_level': Level.inst().get_layer_level(),
                               'layer_entity': Level.inst().get_layer_entity_playerless()},
                              sort_keys=True, indent=4, cls=EncodeLevelObject)
            print(f"Exported room as {name_file}_{str(id_file)}.json")
            f.write(data)
            f.close()

    @staticmethod
    @Event.trigger(Events.ROOM_LOADED)
    def import_room(name):
        from level.level import Level

        level = Level.inst()

        try:
            with open("assets/rooms/" + name + '.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                layer_bg = data["layer_background"]
                layer_level = data["layer_level"]
                layer_entity = data["layer_entity"]

                level.cleanse_level()
                level.cleanse_background()
                level.cleanse_entity_playerless()

                for obj in layer_bg:
                    o = Engine.inst().create_import_obj(obj)
                    if o is not None:
                        level.add_background(o)
                for obj in layer_level:
                    o = Engine.inst().create_import_obj(obj)
                    if o is not None:
                        level.add_level(o)
                for obj in layer_entity:
                    print(obj)
                    if obj["type"] not in ("PlayerBig", "PlayerSmall"):
                        o = Engine.inst().create_import_obj(obj)
                        if o is not None:
                            level.add_entity(o)

                f.close()
        except FileNotFoundError:
            print(colored(f"Could not find room file: assets/rooms/{name}.json"))

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
        reg = Engine.inst().registries
        cs, _ = reg[name]
        return cs
import pygame as pg
import config as c
from _devtools.level_editor.terrain.editor_terrain_selected import EditorTerrainSelected
from datatype.coordinate_screen import CoordinateScreen
from engine import Engine
from entity.concrete.player.player_entity import PlayerEntity
from event_handler.events import Events
from level.level import Level
from overlay.menu import Menu
from event_handler.event_handler import Event
from terrain.concrete.terrain.camera_cutoff import CameraCutoff


class TerrainPickController(Menu):
    _instance = None

    def __init__(self):
        super().__init__(CoordinateScreen(0, 0))
        self.prev_pressed = False
        self.collided = []
        self.terrain_prev = None

        Level.get_instance().add_overlay(self)
        TerrainPickController._instance = self

    @classmethod
    def create_name(cls):
        return "terrain_pick_controller"

    def create_image(self):
        pass

    def create_texture(self, colorkey_custom="black"):
        pass

    def create_content(self):
        return []

    @classmethod
    def create_texture_size(cls):
        return 0, 0

    @staticmethod
    def get_instance():
        return TerrainPickController._instance

    @staticmethod
    @Event.listener(Events.EDITOR_TERRAIN_CREATED, Event.When.BEFORE)
    def revert_terrain(_):
        if TerrainPickController.get_instance().terrain_prev is not None:
            layer, obj = TerrainPickController.get_instance().terrain_prev
            layer.append(obj)

    def update(self):
        if pg.mouse.get_pressed()[c.KEY_EDITING_PICK]:
            if not self.prev_pressed:
                if self.terrain_prev is not None:
                    layer, obj = self.terrain_prev
                else:
                    layer, obj = None, None
                terrain = self.pick_terrain()

                if terrain is not None:
                    if not EditorTerrainSelected.get_instance() is None:
                        if layer is not None and obj is not None:
                            layer.append(obj)
                        EditorTerrainSelected.get_instance().scrap()
                    obj = EditorTerrainSelected(type(terrain), terrain.pos)
                    vars_t = dict(vars(terrain))
                    vars_t.pop("pos")
                    obj.scaler = terrain.scaler
                    vars_t.pop("scaler")
                    obj.rot = terrain.rot
                    vars_t.pop("rot")
                    obj.change_size(terrain.size)
                    vars_t.pop("size")
                    vars_t.pop("image")
                    vars_t.pop("collider")
                    obj.vars = vars_t
                    Level.get_instance().add_level_entity(obj)

                self.prev_pressed = True
        elif self.prev_pressed:
            self.prev_pressed = False

    def pick_terrain(self):
        collided = []
        terrains = [o for o in Level.get_instance().get_terrain_all()
                    if not type(o).__name__ == "EditorTerrainSelected"
                    and not type(o).__name__ == "PlayerEntity"
                    and (Engine.key_mod_down(c.KEY_SUBTLE_EDITING) or not type(o).__name__ == "CameraCutoff")]
        for obj in terrains:
            if obj.collider.collide(CoordinateScreen(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]).convert_to_world().tuple(),
                                    True, [c.KEY_EDITING_PICK]):
                collided.append(obj)
        self.collided = [o for o in self.collided if any(o is x for x in collided)]
        for obj in collided:
            if obj not in self.collided:
                self.collided.append(obj)
        if len(collided) == 0:
            return

        terrain = self.collided.pop(0)
        for layer in (Level.get_instance().layer_background, Level.get_instance().layer_level,
                      Level.get_instance().layer_level_entity, Level.get_instance().layer_entity):
            if terrain in layer:
                self.terrain_prev = layer, terrain
                layer.remove(terrain)
        return terrain
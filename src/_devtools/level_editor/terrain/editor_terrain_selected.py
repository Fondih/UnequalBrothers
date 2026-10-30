import inspect
from abc import ABC

import pygame as pg

import config as c
from _devtools.level_editor.overlay.editor_terrain_menu import menu_type_registry
from _devtools.level_editor.overlay.editor_terrain_menu.menus import Menus
from collider.collider import Collider
from collider.colliders.rect_collider import RectCollider
from datatype.coordinate import Coordinate
from datatype.coordinate_screen import CoordinateScreen
from engine import Engine
from entity.entity import Entity
from event_handler.event_handler import Event
from event_handler.events import Events
from level.dt import Dt
from level.level import Level
from terrain.level_entity import LevelEntity
from terrain.terrain import Terrain


class EditorTerrainSelected(LevelEntity, ABC):
    _instance = None
    edit_list = []

    def __init__(self, type_obj, pos):
        if EditorTerrainSelected._instance is not None:
            raise RuntimeError("Editor terrain selected already exists - use EditorTerrainSelected.get_instance() instead")

        self.type_obj = type_obj
        EditorTerrainSelected._instance = self  # temp as fix for bug if removed

        super().__init__(pos)

        self.menu = self.create_menu()
        self.is_held = False
        self.held_offset = pg.Vector2(0, 0)
        self.painted_flag = False
        self.paint_commit_last = None
        self.paint_pos_offset = pg.Vector2(0, 0)

        EditorTerrainSelected._instance = self

    @classmethod
    def create_name(cls):
        return cls._instance.type_obj.create_name()

    @classmethod
    def is_colliding(cls):
        return False

    @classmethod
    def create_namespace(cls):
        return cls._instance.type_obj.create_namespace()

    @classmethod
    def create_pos_offset(cls, scaler):
        return cls.get_instance().type_obj.create_pos_offset(scaler)

    @classmethod
    def create_texture_size(cls):
        return cls._instance.type_obj.create_texture_size()

    def create_collider(self):
        return RectCollider((self.pos + self.create_pos_offset(self.scaler)).convert_to_surface(), self.get_texture_size_scaled(self.scaler), Collider.Type.MOUSE, is_solid=False, buttons_mouse=[c.KEY_EDITING_DRAG, c.KEY_EDITING_PAINT])

    def create_menu(self):
        try:
            menu_type = menu_type_registry.get(self.type_obj).value
        except KeyError:
            menu_type = Menus.DEFAULT.value

        x, y = self.get_texture_size_scaled(self.scaler)
        menu = menu_type((self.pos + pg.Vector2(x / 2, 0)).convert_to_surface())
        Level.get_instance().add_overlay(menu)
        return menu

    def change_pos(self, pos):
        self.pos = pos
        self.collider.update_pos((pos + self.create_pos_offset(self.scaler)).convert_to_surface())

    @staticmethod
    @Event.listener(Events.PLAYER_MOVE, Event.When.AFTER)
    def player_moved(player, dist):
        try:
            EditorTerrainSelected._instance.collider = EditorTerrainSelected._instance.create_collider()
        except AttributeError:
            pass

    @staticmethod
    def snap(value, grid, offset=0):
        return round((value - offset) / grid) * grid + offset

    def update(self):
        super().update()

        if self.paint_commit_last is not None and not pg.mouse.get_pressed()[c.KEY_EDITING_PAINT]:
            self.paint_pos_offset = pg.Vector2(0, 0)
            self.paint_commit_last = None
            self.painted_flag = False

        m_x, m_y = pg.mouse.get_pos()
        m_pos = CoordinateScreen(m_x, m_y)

        if pg.mouse.get_pressed()[c.KEY_EDITING_PAINT]:
            grid_x, grid_y = self.get_texture_size_scaled(self.scaler)
        else:
            grid_x, grid_y = (c.GRID_SIZE, c.GRID_SIZE)

        if self.is_held:
            x, y = (m_pos - self.held_offset).convert_to_world().tuple()
            if not Engine.key_mod_down(c.KEY_SUBTLE_EDITING):
                if not self.painted_flag and pg.mouse.get_pressed()[c.KEY_EDITING_PAINT]:
                    self.paint_pos_offset = pg.Vector2(self.pos.x % grid_x, self.pos.y % grid_y)
                    self.painted_flag = True

                x = self.snap(x, grid_x, self.paint_pos_offset.x)
                y = self.snap(y, grid_y, self.paint_pos_offset.y)
            pos = Coordinate(x, y)

            self.change_pos(pos)
        if self.collider.collide(pg.mouse.get_pos()):
            if not self.is_held:
                self.held_offset = m_pos - self.pos.convert_to_surface()
                self.is_held = True


        if self.is_held and not self.collider.button_held():
            self.is_held = False


        s_x, s_y = self.get_texture_size_scaled(self.scaler)
        o_vec = pg.Vector2(s_x // 2, 0)
        self.menu.change_pos((self.pos + o_vec + self.menu.create_offset() + self.create_pos_offset(self.scaler)).convert_to_surface())

        if pg.mouse.get_pressed()[c.KEY_EDITING_PAINT]:
            if (self.paint_commit_last is None or
                    (abs(self.pos.x - self.paint_commit_last.x) >= s_x or
                     abs(self.pos.y - self.paint_commit_last.y) >= s_y)):
                self.commit_copy()
                self.paint_commit_last = self.pos

    def enlarge(self):
        size_x, size_y = self.get_texture_size_scaled(self.scaler)

        if Engine.key_mod_down(c.KEY_SUBTLE_EDITING):
            size_x_target = size_x + c.GRID_SIZE // 5
        else:
            size_x_target = size_x - size_x % c.GRID_SIZE + c.GRID_SIZE

        scaler = size_x_target / size_x

        self.scaler *= scaler

        self.image = self.create_image()
        self.collider = self.create_collider()

    def shrink(self):
        size_x, size_y = self.get_texture_size_scaled(self.scaler)

        if Engine.key_mod_down(c.KEY_SUBTLE_EDITING):
            size_x_target = size_x - c.GRID_SIZE // 5
        else:
            size_x_target = size_x
            if size_x % c.GRID_SIZE == 0:
                size_x_target -= c.GRID_SIZE
            else:
                size_x_target -= size_x % c.GRID_SIZE + c.GRID_SIZE


        scaler = size_x_target / size_x
        if not scaler < 0.01:
            self.scaler *= scaler

            self.image = self.create_image()
            self.collider = self.create_collider()

    def rotate(self, rot):
        self.rot -= rot
        self.collider.rotate(rot)
        self.image = self.create_image()

    def scrap(self):
        Level.get_instance().get_layer_overlay().remove(self.menu)
        Level.get_instance().get_layer_level_entity().remove(self)
        self.scrap_texture()
        self.scrap_instance()

    @staticmethod
    def get_missing_args(type_obj, already_supplied=('pos', 'scaler', 'rot')):
        sig = inspect.signature(type_obj)
        missing = []

        for name, param in sig.parameters.items():
            if name in already_supplied:
                continue
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue
            if param.default is inspect.Parameter.empty:
                missing.append(param)

        return missing

    @staticmethod
    def prompt_for_missing_args(missing_params):
        kwargs = {}

        for param in missing_params:
            type_hint = param.annotation if param.annotation is not inspect.Parameter.empty else str
            type_name = getattr(type_hint, '__name__', 'value')

            with Dt.get_instance().forcepause():
                raw = input(f"'{param.name}' requires a value ({type_name}): ")

            try:
                kwargs[param.name] = type_hint(raw) if callable(type_hint) else raw
            except (TypeError, ValueError):
                print(f"  couldn't convert '{raw}' to {type_name}, keeping it as text")
                kwargs[param.name] = raw

        return kwargs

    def commit(self):
        missing = self.get_missing_args(self.type_obj)
        extra_kwargs = self.prompt_for_missing_args(missing) if missing else {}

        obj = self.type_obj(pos=self.pos, scaler=self.scaler, rot=self.rot, **extra_kwargs)

        if isinstance(obj, Terrain):
            Level.get_instance().add_level(obj)
            Engine.render_terrain()
            self.edit_list.append(obj)
        if isinstance(obj, LevelEntity):
            Level.get_instance().add_level_entity(obj)
            self.edit_list.append(obj)
        if isinstance(obj, Entity):
            Level.get_instance().add_entity(obj)
            self.edit_list.append(obj)

        self.scrap()

    def commit_copy(self):
        missing = self.get_missing_args(self.type_obj)
        extra_kwargs = self.prompt_for_missing_args(missing) if missing else {}

        obj = self.type_obj(pos=self.pos, scaler=self.scaler, rot=self.rot, **extra_kwargs)

        if isinstance(obj, Terrain) and self.commit_needed(Level.get_instance().get_layer_level(), obj):
            Level.get_instance().add_level(obj)
            Engine.render_terrain()
            self.edit_list.append(obj)
        if isinstance(obj, LevelEntity) and self.commit_needed(Level.get_instance().get_layer_level_entity(), obj):
            Level.get_instance().add_level_entity(obj)
            self.edit_list.append(obj)
        if isinstance(obj, Entity) and self.commit_needed(Level.get_instance().get_layer_entity(), obj):
            Level.get_instance().add_entity(obj)
            self.edit_list.append(obj)

    def commit_needed(self, layer, obj):
        return not any(e == obj for e in layer if e is not self)

    @classmethod
    def undo_commit(cls):
        if len(cls.edit_list) > 0:
            item = cls.edit_list.pop(-1)
            if isinstance(item, Terrain):
                if Level.get_instance().get_layer_level().__contains__(item):
                    Level.get_instance().get_layer_level().remove(item)
                    Engine.render_terrain()
            if isinstance(item, LevelEntity):
                if Level.get_instance().get_layer_level_entity().__contains__(item):
                    Level.get_instance().get_layer_level_entity().remove(item)
            if isinstance(item, Entity):
                if Level.get_instance().get_layer_entity().__contains__(item):
                    Level.get_instance().get_layer_entity().remove(item)

    @classmethod
    def scrap_instance(cls):
        cls._instance = None

    @classmethod
    def get_instance(cls):
        return cls._instance

    @staticmethod
    @Event.listener(Events.ROOM_LOADED)
    def room_changed(name, namespace=None):
        EditorTerrainSelected.get_instance().scrap()
import inspect
from abc import ABC

import pygame as pg

import config as c
from _devtools.level_editor.overlay.editor_terrain_menu import menu_type_registry
from _devtools.level_editor.overlay.editor_terrain_menu.editor_terrain_selected_info_menu import \
    EditorTerrainSelectedInfoMenu
from collider.collider import Collider
from collider.colliders.rect_collider import RectCollider
from datatype.coordinate import Coordinate
from datatype.coordinate_screen import CoordinateScreen
from engine import Engine
from entity.entity import Entity
from event_handler.event_handler import Event
from event_handler.events import Events
from level.camera import Camera
from level.dt import Dt
from level.level import Level
from terrain.terrain import Terrain
from utils.nine_slice import nine_slice


class EditorTerrainSelected(Terrain, ABC):
    _instance = None
    edit_list = []

    def __init__(self, type_obj, pos):
        if EditorTerrainSelected._instance is not None:
            raise RuntimeError("Editor terrain selected already exists - use EditorTerrainSelected.get_instance() instead")

        self.type_obj = type_obj
        EditorTerrainSelected._instance = self  # temp as fix for bug if removed

        super().__init__(pos, solid=False)

        self.menu = self.create_menu()
        self.info_menu = self.create_info_menu()
        self.is_held = False
        self.held_offset = pg.Vector2(0, 0)
        self.painted_flag = False
        self.paint_commit_last = None
        self.paint_pos_offset = pg.Vector2(0, 0)
        self.resize = False
        self.start_size = (0, 0)
        self.start_mouse = (0, 0)
        self.vars = {}

        EditorTerrainSelected._instance = self

    @classmethod
    def create_name(cls):
        return cls._instance.type_obj.create_name()

    @classmethod
    def has_alpha(cls):
        return cls.get_instance().type_obj.has_alpha()

    @classmethod
    def colorkey(cls):
        return cls.get_instance().type_obj.colorkey()

    def set_resize(self, state):
        self.resize = bool(state)

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
        return RectCollider((self.pos + self.create_pos_offset(self.scaler)).convert_to_surface(Engine.inst().cams["big"]), self.get_texture_size_scaled(self.scaler), Collider.Type.MOUSE, is_solid=False, buttons_mouse=[c.KEY_EDITING_DRAG, c.KEY_EDITING_PAINT])

    def create_menu(self):
        from _devtools.level_editor.overlay.editor_terrain_menu.menus import Menus

        try:
            menu_type = menu_type_registry.get(self.type_obj).value
        except KeyError:
            menu_type = Menus.DEFAULT.value

        x, y = self.get_texture_size_scaled(self.scaler)
        menu = menu_type((self.pos + pg.Vector2(x / 2, 0)).convert_to_surface(Engine.inst().cams["big"]))
        Level.inst().add_overlay(menu)
        return menu

    def change_pos(self, pos):
        self.pos = pos
        self.collider.update((pos + self.create_pos_offset(self.scaler)).convert_to_surface(Engine.inst().cams["big"]))

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

        if pg.key.get_pressed()[c.KEY_DISCARD_SELECTED]:
            self.scrap()
            return
        if pg.key.get_pressed()[c.KEY_COMMIT_SELECTED]:
            self.commit()
            self.scrap()
            return

        m_x, m_y = pg.mouse.get_pos()
        m_pos = CoordinateScreen(m_x, m_y).convert_to_world(Engine.inst().cams["big"])

        if self.resize:
            grid_x, grid_y = (c.GRID_SIZE, c.GRID_SIZE)

            if self.is_held:
                start_sx, start_sy = self.start_size
                d_x, d_y = (m_pos - self.start_mouse).tuple()

                sx = start_sx + d_x
                sy = start_sy + d_y

                if not Engine.key_mod_down(c.KEY_SUBTLE_EDITING):
                    sx = self.snap(sx, grid_x)
                    sy = self.snap(sy, grid_y)

                sx = max(sx, grid_x)
                sy = max(sy, grid_y)

                self.change_size((sx, sy))
            if self.collider.collide(pg.mouse.get_pos()):
                if not self.is_held:
                    self.start_mouse = m_pos
                    self.start_size = self.size
                    self.is_held = True

            if self.is_held and not self.collider.button_held():
                self.is_held = False

            s_x, s_y = self.get_texture_size_scaled(self.scaler)
            o_vec = pg.Vector2(s_x // 2, 0)
            self.menu.change_pos((self.pos + o_vec + self.menu.create_offset() + self.create_pos_offset(
                self.scaler)).convert_to_surface(Engine.inst().cams["big"]))

        else:
            if pg.mouse.get_pressed()[c.KEY_EDITING_PAINT]:
                grid_x, grid_y = self.get_texture_size_scaled(self.scaler)
            else:
                grid_x, grid_y = (c.GRID_SIZE, c.GRID_SIZE)

            if self.paint_commit_last is not None and not pg.mouse.get_pressed()[c.KEY_EDITING_PAINT]:
                self.paint_pos_offset = pg.Vector2(0, 0)
                self.paint_commit_last = None
                self.painted_flag = False

            if self.is_held:
                x, y = (m_pos - self.held_offset).tuple()
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
                    self.held_offset = m_pos - self.pos
                    self.is_held = True


            if self.is_held and not self.collider.button_held():
                self.is_held = False


            s_x, s_y = self.get_texture_size_scaled(self.scaler)
            o_vec = pg.Vector2(s_x // 2, 0)
            self.menu.change_pos((self.pos + o_vec + self.menu.create_offset() + self.create_pos_offset(self.scaler)).convert_to_surface(Engine.inst().cams["big"]))

            if pg.mouse.get_pressed()[c.KEY_EDITING_PAINT]:
                if (self.paint_commit_last is None or
                        (abs(self.pos.x - self.paint_commit_last.x) >= s_x or
                         abs(self.pos.y - self.paint_commit_last.y) >= s_y)):
                    self.commit()
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
        from _devtools.level_editor.overlay.controllers.terrain_pick_controller import TerrainPickController


        Level.inst().layer_overlay.remove(self.menu)
        Level.inst().layer_overlay.remove(self.info_menu)
        self.info_menu.scrap()
        try:
            Level.inst().remove(self, Level.inst().layer_level)
        except ValueError:
            pass
        self.scrap_texture()
        self.scrap_instance()
        TerrainPickController.inst().terrain_prev = None

    def get_missing_args(self, type_obj, already_supplied=('pos', 'scaler', 'rot')):
        sig = inspect.signature(type_obj)
        missing = []

        for name, param in sig.parameters.items():
            if name in already_supplied or name in self.vars.keys():
                continue
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue
            if param.default is inspect.Parameter.empty:
                missing.append(param)

        return missing

    @classmethod
    def split_init_vars(cls, class_, state):
        params = inspect.signature(class_).parameters
        init_kwargs = {k: v for k, v in state.items() if k in params}
        leftover = {k: v for k, v in state.items() if k not in params}
        return init_kwargs, leftover

    @staticmethod
    def prompt_for_missing_args(missing_params):
        kwargs = {}

        for param in missing_params:
            type_hint = param.annotation if param.annotation is not inspect.Parameter.empty else str
            type_name = getattr(type_hint, '__name__', 'value')

            with Dt.inst().forcepause():
                raw = input(f"'{param.name}' requires a value ({type_name}): ")

            try:
                kwargs[param.name] = type_hint(raw) if callable(type_hint) else raw
            except (TypeError, ValueError):
                print(f"  couldn't convert '{raw}' to {type_name}, keeping it as text")
                kwargs[param.name] = raw

        return kwargs

    def commit(self):
        missing = self.get_missing_args(self.type_obj)
        args = self.prompt_for_missing_args(missing) if missing else {}
        args = self.vars | args

        extra_kwargs, _ = self.split_init_vars(self.type_obj, args)

        obj = self.type_obj(pos=self.pos, scaler=self.scaler, rot=self.rot, **extra_kwargs)
        obj.change_size(self.size)

        if isinstance(obj, Terrain):
            Level.inst().add_level(obj)
            self.edit_list.append(obj)
        if isinstance(obj, Entity):
            Level.inst().add_entity(obj)
            self.edit_list.append(obj)

    def commit_needed(self, layer, obj):
        return not any(e == obj for e in layer if e is not self)

    @classmethod
    def undo_commit(cls):
        if len(cls.edit_list) > 0:
            item = cls.edit_list.pop(-1)
            if isinstance(item, Terrain):
                if Level.inst().layer_level.__contains__(item):
                    Level.inst().remove(item, Level.inst().layer_level)
            if isinstance(item, Entity):
                if Level.inst().layer_entity.__contains__(item):
                    Level.inst().remove(item, Level.inst().layer_entity)

    @classmethod
    def scrap_instance(cls):
        cls._instance = None

    @classmethod
    def get_instance(cls):
        return cls._instance

    @staticmethod
    @Event.listener(Events.ROOM_LOADED)
    def room_changed(name, namespace=None):
        try:
            EditorTerrainSelected.get_instance().scrap()
        except AttributeError:
            pass

    def create_image(self):
        if self.type_obj.__name__ == "CameraCutoff":
            img = self.get_texture()
            sx, sy = self.size
            sx *= self.scaler * Camera.zoom()
            sy *= self.scaler * Camera.zoom()

            img = nine_slice(img, (sx, sy), (25, 25, 25, 25))
            if not self.rot == 0:
                img = pg.transform.rotate(img, self.rot)
        else:
            img = self.type_obj.create_image(self)

        pg.draw.rect(img, "yellow", ((0, 0), img.get_size()), 3 * Camera.zoom())
        return img

    def create_info_menu(self):
        x, y = EditorTerrainSelectedInfoMenu.create_texture_size()
        menu = EditorTerrainSelectedInfoMenu(CoordinateScreen(10, c.HEIGHT - y - 10), self.type_obj)
        Level.inst().add_overlay(menu)
        return menu
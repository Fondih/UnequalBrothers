from abc import ABC

import pygame as pg

from _devtools.level_editor.overlay.editor_terrain_menu import menu_type_registry
from _devtools.level_editor.overlay.editor_terrain_menu.menus import Menus
from engine import Engine
from level.camera import Camera
from run_modes import RunModes
from terrain.terrain import Terrain
from terrain.terrain_registry import register
from utils.nine_slice import nine_slice


@menu_type_registry.spec_menu(Menus.RESIZABLE_RECT)
@register(["level utils"])
class CameraCutoff(Terrain, ABC):
    def __init__(self, pos, scaler=1, rot=0):
        super().__init__(pos, scaler=scaler, rot=rot, solid=False)

    @classmethod
    def create_name(cls):
        if Engine.inst().run_mode == RunModes.EDITOR:
            return "camera_cutoff_shown"
        else:
            return "camera_cutoff"

    @classmethod
    def create_texture_size(cls):
        return 50, 50

    def create_image(self):
        pass

    def render(self, screen, cam, zoom):
        if Engine.inst().run_mode != RunModes.EDITOR:
            return
        cs_x, cs_y = cam.size
        x = (self.pos.x - cam.pos.x) * zoom + cs_x / 2
        y = (self.pos.y - cam.pos.y) * zoom + cs_y / 2
        w = self.size[0] * self.scaler * zoom
        h = self.size[1] * self.scaler * zoom
        if x > cs_x or y > cs_y or x + w < 0 or y + h < 0:
            return
        pg.draw.rect(screen, "yellow", (x, y, w, h), max(1, int(3 * zoom)))
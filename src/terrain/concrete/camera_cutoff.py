from abc import ABC

import pygame as pg

from _devtools.level_editor.overlay.editor_terrain_menu import menu_type_registry
from _devtools.level_editor.overlay.editor_terrain_menu.menus import Menus
from collider.collider import Collider
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
        if Engine.get_instance().run_mode == RunModes.EDITOR:
            return "camera_cutoff_shown"
        else:
            return "camera_cutoff"

    @classmethod
    def create_texture_size(cls):
        return 50, 50

    def create_image(self):
        if Engine.get_instance().run_mode == RunModes.EDITOR:
            img = self.get_texture()
            sx, sy = self.size
            sx *= self.scaler * Camera.get_instance().zoom
            sy *= self.scaler * Camera.get_instance().zoom

            img = nine_slice(img, (sx, sy), (25, 25, 25, 25))
            if not self.rot == 0:
                img = pg.transform.rotate(img, self.rot)

            self.image = img
            return img
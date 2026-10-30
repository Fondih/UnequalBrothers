import pygame as pg

import src.config as c
from _devtools.level_editor.overlay.editing_menu.terrain_folder_lever import TerrainFolderLever
from overlay.menu import Menu


class TerrainPlaceMenu(Menu):
    def __init__(self, pos):
        super().__init__(pos)

    @classmethod
    def create_name(cls):
        return "terrain_place_menu"

    @classmethod
    def create_texture_size(cls):
        return 300, c.HEIGHT - 110

    def create_texture(self, colorkey_custom="black"):
        texture = pg.Surface(self.get_texture_size_scaled(), pg.SRCALPHA, 32)
        texture.convert_alpha()
        texture.fill((90, 90, 90, 100))

        return texture

    def create_content(self):
        pos_root = self.pos + pg.Vector2(10, 10)
        terrain_lever = TerrainFolderLever(pos_root, ["terrain"], pos_root)
        content = [terrain_lever]
        return content

    def toggled_event(self):
        if self.shown:
            for obj in self.content:
                obj.set_state(1)
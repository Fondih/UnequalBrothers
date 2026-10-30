from abc import ABC
import pygame as pg
from _devtools.level_editor.overlay.editing_menu.terrain_place_menu import TerrainPlaceMenu
from collider.collider import Collider
from collider.colliders.rect_collider import RectCollider
from overlay.lever import Lever


class TerrainPlaceLever(Lever, ABC):
    def __init__(self, pos):
        super().__init__(pos)

        self.menu = self.create_menu()

    @classmethod
    def create_name(cls):
        return "terrain_place_lever"

    @classmethod
    def create_texture_size(cls):
        return 50, 50

    def create_collider(self):
        return RectCollider(self.pos, self.get_texture_size_scaled(), Collider.Type.MOUSE, is_solid=False)


    def create_menu(self):
        return TerrainPlaceMenu(self.pos + pg.Vector2(-250, 70))

    def clicked(self):
        self.menu.toggle_shown()
from abc import ABC

from _devtools.level_editor.overlay.grid.grid_visual_menu import GridVisualMenu
from collider.collider import Collider
from collider.colliders.rect_collider import RectCollider
from level.level import Level
from overlay.lever import Lever


class GridVisualMenuLever(Lever, ABC):
    def __init__(self, pos):
        super().__init__(pos)

        self.menu = self.create_menu()

    @classmethod
    def create_name(cls):
        return "grid_visual_menu_lever"

    @classmethod
    def create_texture_size(cls):
        return 30, 30

    def create_collider(self):
        return RectCollider(self.pos, self.get_texture_size_scaled(), Collider.Type.MOUSE, is_solid=False)

    def create_menu(self):
        menu = GridVisualMenu(self.pos)
        Level.get_instance().add_overlay(menu)
        return menu

    def clicked(self):
        super().clicked()

        self.menu.toggle_shown()
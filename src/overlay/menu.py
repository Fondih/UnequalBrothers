from abc import ABC

from collider.collider import Collider
from overlay.screen_object import ScreenObject


class Menu(ScreenObject, ABC):
    def __init__(self, pos, scaler=1, rot=0):
        super().__init__(pos, scaler, rot)
        self.shown = False
        self.content = self.create_content()

    @classmethod
    def create_name(cls):
        return "editor_terrain_menu"

    def set_shown(self, shown):
        self.shown = shown
        self.toggled_event()

    def toggle_shown(self):
        self.shown = not self.shown
        self.toggled_event()

    @staticmethod
    def create_content():
        return []

    def create_collider(self):
        return Collider(self.pos, Collider.Type.MOUSE, is_solid=False)  # to avoid potential bugs

    def render(self, layer):
        if self.shown:
            if self.image is not None:
                layer.blit(self.image, self.pos.tuple())

            for obj in self.content:
                obj.render(layer)

    def toggled_event(self):
        pass

    def update(self):
        if not self.shown:
            return

        for obj in self.content:
            obj.update()
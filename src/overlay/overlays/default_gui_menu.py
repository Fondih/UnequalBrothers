from abc import ABC

from overlay.menu import Menu
from overlay.overlays.fps_display import FPSDisplay


class DefaultGuiMenu(Menu, ABC):
    def __init__(self, pos):
        super().__init__(pos)

        self.shown = True

    @classmethod
    def create_name(cls):
        return "default_gui_menu"

    def create_texture(self, colorkey_custom="black"):
        pass

    def create_image(self):
        pass

    @classmethod
    def create_texture_size(cls):
        return 0, 0

    def create_content(self):
        return [FPSDisplay()]
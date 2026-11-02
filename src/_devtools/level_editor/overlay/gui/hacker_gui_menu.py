from abc import ABC

import config as c

from _devtools.level_editor.overlay.gui.noclip_lever import NoclipLever
from datatype.coordinate_screen import CoordinateScreen
from overlay.menu import Menu
from overlay.overlays.fps_display import FPSDisplay


class HackerGuiMenu(Menu, ABC):
    def __init__(self, pos):
        super().__init__(pos)

        self.shown = True

    @classmethod
    def create_name(cls):
        return "hacker_gui_menu"

    def create_texture(self, colorkey_custom="black"):
        pass

    def create_image(self):
        pass

    @classmethod
    def create_texture_size(cls):
        return 0, 0

    def create_content(self):
        return [NoclipLever(CoordinateScreen(c.WIDTH - 60, 30)),
                FPSDisplay()]
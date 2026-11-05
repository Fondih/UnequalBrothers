from abc import ABC

from datatype.coordinate_screen import CoordinateScreen
from engine import Engine
from overlay.text import Text
from run_modes import RunModes


class FPSDisplay(Text, ABC):
    def __init__(self):
        pos = CoordinateScreen(20, 65) if Engine.inst().run_mode == RunModes.EDITOR else CoordinateScreen(0, 0)

        super().__init__("", "black", pos, (0, 30))

    @classmethod
    def create_name(cls):
        return "fps_display"

    @classmethod
    def create_texture_size(cls):
        return 0, 30

    def update(self):
        self.text = str(Engine.inst().clock.get_fps())[:3]
        self.image = self.create_image()
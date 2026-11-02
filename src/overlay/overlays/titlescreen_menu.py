from abc import ABC
import config as c
from datatype.coordinate_screen import CoordinateScreen
from overlay.menu import Menu
from overlay.overlays.fps_display import FPSDisplay
from overlay.overlays.start_game_button import StartGameButton
from overlay.overlays.start_game_editor_button import StartGameEditorButton


class TitlescreenMenu(Menu, ABC):
    def __init__(self, pos):
        super().__init__(pos)

        self.shown = True

    @classmethod
    def create_name(cls):
        return "titlescreen_menu"

    def create_texture(self, colorkey_custom="black"):
        pass

    def create_image(self):
        pass

    @classmethod
    def create_texture_size(cls):
        return 0, 0

    def create_content(self):
        return [StartGameButton(CoordinateScreen(c.WIDTH / 2 - 150, c.HEIGHT / 2 - 35)),
                StartGameEditorButton(CoordinateScreen(c.WIDTH / 2 - 150, c.HEIGHT / 2 + 65))]
from abc import ABC
import config as c

from collider.collider import Collider
from collider.colliders.rect_collider import RectCollider
from engine import Engine
from overlay.button import Button
from run_modes import RunModes


class StartGameButton(Button, ABC):
    def __init__(self, pos, scaler=1):
        super().__init__(pos, scaler=scaler)

    @classmethod
    def create_name(cls):
        return "start_game_button"

    @classmethod
    def create_texture_size(cls):
        return 300, 70

    def create_collider(self):
        return RectCollider(self.pos, self.get_texture_size_scaled(), Collider.Type.MOUSE, is_solid=False)

    def clicked(self):
        Engine.get_instance().activate_game(RunModes.DEFAULT, c.ROOM_START)
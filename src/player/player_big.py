from abc import ABC

import src.config as c
from entity.entity_registry import register
from player.player_entity import PlayerEntity


@register(["player"])
class PlayerBig(PlayerEntity, ABC):
    _instance = None

    def __init__(self, pos, scaler=1, rot=0):
        if PlayerBig._instance is not None:
            raise RuntimeError("Player already exists - use Player.get_instance() instead")

        super().__init__(pos, scaler, rot=rot)
        PlayerBig._instance = self

    @classmethod
    def health_max(cls):
        return 100

    @classmethod
    def has_alpha(cls):
        return True

    @classmethod
    def colorkey(cls):
        return "black"

    @classmethod
    def create_texture_size(cls):
        return 45, 60

    @classmethod
    def create_name(cls):
        return "player_big"

    @staticmethod
    def get_input_keys():
        return c.K_UP_B, c.K_DOWN_B, c.K_LEFT_B, c.K_RIGHT_B

    @classmethod
    def inst(cls):
        return cls._instance
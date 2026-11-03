from abc import ABC

import src.config as c
from entity.entity_registry import register
from player.player_entity import PlayerEntity


@register(["player"])
class PlayerSmall(PlayerEntity, ABC):
    _instance = None

    def __init__(self, pos, scaler=1, rot=0):
        if PlayerSmall._instance is not None:
            raise RuntimeError("Player already exists - use Player.get_instance() instead")

        super().__init__(pos, scaler, rot=rot)
        PlayerSmall._instance = self

    @classmethod
    def health_max(cls):
        return 100

    @classmethod
    def create_texture_size(cls):
        return 64, 60

    @classmethod
    def create_name(cls):
        return "player_small"

    @staticmethod
    def get_input_keys():
        return c.K_UP_S, c.K_DOWN_S, c.K_LEFT_S, c.K_RIGHT_S

    @classmethod
    def get_instance(cls):
        return cls._instance
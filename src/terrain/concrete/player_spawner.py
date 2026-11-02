from abc import ABC

import pygame as pg

from collider.collider import Collider
from engine import Engine
from run_modes import RunModes
from terrain.terrain import Terrain
from terrain.terrain_registry import register


@register(["level utils"])
class PlayerSpawner(Terrain, ABC):
    def __init__(self, pos, spawner_id: int, scaler=1, rot=0):
        super().__init__(pos, scaler=scaler, rot=rot, solid=False)

        self.spawner_id = spawner_id

    @classmethod
    def create_name(cls):
        if Engine.get_instance().run_mode == RunModes.EDITOR:
            return "player_spawner_shown"
        else:
            return "player_spawner"

    @classmethod
    def create_texture_size(cls):
        return 50, 50

    def get_player_spawn_pos(self):
        x, y = self.get_texture_size_scaled(self.scaler)
        x /= 2

        return self.pos + pg.Vector2(x, y)
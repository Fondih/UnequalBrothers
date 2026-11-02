from abc import ABC

from collider.collider import Collider
from terrain.terrain import Terrain
from terrain.terrain_registry import register


@register(["floor"])
class FloorStone(Terrain, ABC):
    def __init__(self, pos, scaler=1, rot=0):
        super().__init__(pos, scaler=scaler, rot=rot, solid=False)

    @classmethod
    def create_name(cls):
        return "floor_stone"

    @classmethod
    def create_texture_size(cls):
        return 50, 50
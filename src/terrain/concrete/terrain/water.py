from abc import ABC
from collider.collider import Collider
from collider.colliders.rect_collider import RectCollider
from terrain.terrain import Terrain
from terrain.terrain_registry import register


@register(["wall"])
class Water(Terrain, ABC):
    def __init__(self, pos, scaler=1, rot=0):
        super().__init__(pos, scaler=scaler, rot=rot)

    @classmethod
    def create_name(cls):
        return "water"

    @classmethod
    def create_texture_size(cls):
        return 50, 50

    def create_collider(self):
        return RectCollider(self.pos, self.get_texture_size_scaled(self.scaler), Collider.Type.LEVEL)
from abc import ABC

from collider.collider import Collider
from collider.colliders.rect_collider import RectCollider
from overlay.lever import Lever


# Currently not implemented, supposed to let you select an already placed
# terrain as EditorTerrainSelected
class SelectTerrainLever(Lever, ABC):
    def __init__(self, pos):
        super().__init__(pos)

    @classmethod
    def create_name(cls):
        return "select_terrain_lever"

    @classmethod
    def create_texture_size(cls):
        return 30, 30

    def create_collider(self):
        return RectCollider(self.pos, self.get_texture_size_scaled(), Collider.Type.MOUSE, is_solid=False)
from abc import ABC

from collider.collider import Collider
from collider.colliders.rect_collider import RectCollider
from entity.concrete.player.player_entity import PlayerEntity
from overlay.lever import Lever


class NoclipLever(Lever, ABC):
    def __init__(self, pos):
        super().__init__(pos)

        self.state = 1 if PlayerEntity.get_instance().noclip else 0

    @classmethod
    def create_name(cls):
        return "noclip_lever"

    @classmethod
    def create_texture_size(cls):
        return 30, 30

    def create_collider(self):
        return RectCollider(self.pos, self.get_texture_size_scaled(), Collider.Type.MOUSE, is_solid=False)

    def clicked(self):
        super().clicked()

        PlayerEntity.get_instance().toggle_noclip()
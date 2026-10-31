from abc import ABC, abstractmethod

from collider.collider import Collider
from entity.entity import Entity
from level.level import Level


class LivingEntity(Entity, ABC):
    def __init__(self, pos, scaler, vel=None, rot=0):
        super().__init__(pos, scaler, vel=vel, rot=rot)

        self.health = self.health_max()

    @classmethod
    @abstractmethod
    def health_max(cls):
        return 1

    @classmethod
    def create_name(cls):
        return "living_entity"

    @abstractmethod
    def create_collider(self):
        return Collider(self.pos, Collider.Type.LEVEL)

    @classmethod
    @abstractmethod
    def create_texture_size(cls):
        return 1, 1

    def kill(self):
        Level.get_instance().get_layer_entity().remove(self)

    def damage(self, dmg):
        self.health -= dmg

        if self.health <= 0:
            self.kill()
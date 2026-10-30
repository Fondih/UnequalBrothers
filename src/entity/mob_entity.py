from abc import ABC, abstractmethod
from collider.collider import Collider
from entity.living_entity import LivingEntity


class Mob(LivingEntity, ABC):
    def __init__(self, pos, scaler, vel=None, rot=0):
        super().__init__(pos, scaler, vel=vel, rot=rot)

    @classmethod
    def create_name(cls):
        return "entity"

    @abstractmethod
    def create_collider(self):
        return Collider(self.pos, Collider.Type.LEVEL)

    @classmethod
    @abstractmethod
    def create_texture_size(cls):
        return 1, 1

    def exec_ai(self):
        pass

    def update(self):
        self.exec_ai()

        super().update()
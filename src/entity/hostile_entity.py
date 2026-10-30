from abc import ABC

from entity.living_entity import LivingEntity


class HostileEntity(LivingEntity, ABC):
    def __init__(self, pos, scaler, vel=None, rot=0):
        super().__init__(pos, scaler, vel=vel, rot=rot)

    @classmethod
    def create_name(cls):
        return "hostile_entity"

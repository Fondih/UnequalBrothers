from abc import ABC
from collider.collider import Collider
from src.terrain.level_object import LevelObject


class Terrain(LevelObject, ABC):
    def __init__(self, pos, scaler=1, rot=0):
        super().__init__(pos, scaler, rot)

    @classmethod
    def create_name(cls):
        return "terrain"

    @classmethod
    def create_namespace(cls):
        return "terrain/terrain/"

    def create_collider(self):
        return Collider(self.pos(), Collider.Type.LEVEL)

    def update(self):
        pass

    def render(self, layer):
        img_pos = self.pos + self.create_pos_offset(self.scaler)
        layer.blit(self.image, img_pos.tuple())

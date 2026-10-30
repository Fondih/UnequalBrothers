from abc import ABC
from collider.collider import Collider
from src.terrain.level_object import LevelObject


class LevelEntity(LevelObject, ABC):
    def __init__(self, pos, scaler=1, rot=0):
        super().__init__(pos, scaler, rot)

    def __eq__(self, other):
        return all([
            type(self) is type(other),
            self.pos == other.pos,
            self.scaler == other.scaler,
            self.rot == other.rot
        ])

    @classmethod
    def create_name(cls):
        return "level_entity"

    @classmethod
    def create_namespace(cls):
        return "terrain/level_entity/"

    def create_collider(self):
        return Collider(self.pos(), Collider.Type.LEVEL)

    def change_pos(self, pos):
        self.pos = pos
        self.collider.update_pos(pos + self.create_pos_offset(self.scaler))

    def update(self):
        pass

    def render(self, layer):
        img_pos = self.pos + self.create_pos_offset(self.scaler)
        layer.blit(self.image, img_pos.tuple())
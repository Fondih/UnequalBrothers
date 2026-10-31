from abc import ABC

from collider.collider import Collider
from src.terrain.level_object import LevelObject


class LevelEntity(LevelObject, ABC):
    def __init__(self, pos, scaler=1, rot=0, solid=True):
        super().__init__(pos, scaler, rot, solid)

    def __eq__(self, other):
        return all([
            type(self) is type(other),
            self.pos == other.pos,
            self.scaler == other.scaler,
            self.rot == other.rot,
            self.solid == other.solid
        ])

    @classmethod
    def create_name(cls):
        return "level_entity"

    @classmethod
    def create_namespace(cls):
        return "terrain/level_entity/"

    def change_pos(self, pos):
        self.pos = pos
        self.collider.update_pos(pos + self.create_pos_offset(self.scaler))

    def update(self):
        pass
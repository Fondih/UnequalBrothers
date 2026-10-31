from abc import ABC
import pygame as pg
from level.dt import Dt
from level.level import Level
from terrain.level_object import LevelObject


class Entity(LevelObject, ABC):
    def __init__(self, pos, scaler, vel=None, rot=0):
        self.vel = vel if vel is not None else pg.Vector2(0, 0)

        super().__init__(pos, scaler, rot)

    @classmethod
    def create_name(cls):
        return "entity"

    @classmethod
    def create_namespace(cls):
        return "entity/"

    def create_pos_offset(self, scaler):
        x, y = self.get_texture_size_scaled(scaler)

        return pg.Vector2(-x / 2, -y)

    def move(self, move):
        move_x, move_y = (move.x, move.y)

        collided_x = []
        collided_y = []

        solids = Level.get_instance().get_solid()

        if not move_x == 0:
            probe_x = move_x if abs(move_x) >= 1 else (1 if move_x > 0 else -1)
            moved_collider_x = self.collider.create_moved_copy(pg.Vector2(probe_x, 0))

            for obj in solids:
                if moved_collider_x.collide(obj.collider):
                    collided_x.append(obj)

        if not move_y == 0:
            probe_y = move_y if abs(move_y) >= 1 else (1 if move_y > 0 else -1)
            moved_collider_y = self.collider.create_moved_copy(pg.Vector2(0, probe_y))

            for obj in solids:
                if moved_collider_y.collide(obj.collider):
                    collided_y.append(obj)

        if len(collided_x) > 0:
            dist_x = None
            for obj in collided_x:
                dist = self.collider.get_distance(obj.collider, 0).x
                if dist_x is None or abs(dist) < abs(dist_x):
                    dist_x = dist
            move.x = dist_x
            self.vel = pg.Vector2(0, self.vel.y)

        if len(collided_y) > 0:
            dist_y = None
            for obj in collided_y:
                dist = self.collider.get_distance(obj.collider, 1).y
                if dist_y is None or abs(dist) < abs(dist_y):
                    dist_y = dist

            move.y = dist_y
            self.vel = pg.Vector2(self.vel.x, 0)

        self.change_pos(self.pos + move)

    def is_grounded(self):
        moved_collider_y = self.collider.create_moved_copy(pg.Vector2(0, 1))

        solids = Level.get_instance().get_solid()

        for obj in solids:
            if moved_collider_y.collide(obj.collider):
                return True
        return False

    def change_pos(self, pos):
        self.pos = pos
        self.collider.update_pos(pos + self.create_pos_offset(self.scaler))

    def update(self):
        dt = Dt.get_instance().get_dt()
        self.move(self.vel)

        super().update()
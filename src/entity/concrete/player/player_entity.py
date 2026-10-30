import math
from abc import ABC
import pygame as pg
import src.config as c
from collider.collider import Collider
from collider.colliders.rect_collider import RectCollider
from engine import Engine
from entity.entity_registry import register
from entity.living_entity import LivingEntity
from event_handler.event_handler import Event
from event_handler.events import Events
from level.dt import Dt
from level.level import Level
from run_modes import RunModes


@register(["player"])
class PlayerEntity(LivingEntity, ABC):
    _instance = None

    def __init__(self, pos, scaler=1, speed=c.PLAYER_SPEED):
        if PlayerEntity._instance is not None:
            raise RuntimeError("Player already exists - use Player.get_instance() instead")

        self.noclip = True if (Engine.get_instance().run_mode == RunModes.EDITOR or
                               Engine.get_instance().run_mode == RunModes.HACKS) else False

        super().__init__(pos, scaler)

        self.speed = speed

        PlayerEntity._instance = self

    @classmethod
    def health_max(cls):
        return 100

    @classmethod
    def create_texture_size(cls):
        return 45, 60

    @classmethod
    def create_name(cls):
        return "player_entity"

    def create_collider(self):
        if self.noclip:
            return Collider(self.pos + self.create_pos_offset(self.scaler), Collider.Type.LEVEL)
        return RectCollider(self.pos + self.create_pos_offset(self.scaler), self.get_texture_size_scaled(self.scaler), Collider.Type.LEVEL, is_solid=False)

    def toggle_noclip(self):
        self.noclip = not self.noclip
        self.collider = self.create_collider()
        self.vel = pg.Vector2(0, 0)

    @staticmethod
    def get_input_keys():
        return c.K_UP, c.K_DOWN, c.K_LEFT, c.K_RIGHT, c.K_JUMP

    def walk(self):
        dt = Dt.get_instance().get_dt()

        K_UP, K_DOWN, K_LEFT, K_RIGHT, K_JUMP = self.get_input_keys()
        keys = pg.key.get_pressed()

        dist = pg.Vector2(0, 0)

        if self.noclip:
            if keys[K_LEFT]:
                dist += pg.Vector2(-self.speed * dt, 0)
            if keys[K_RIGHT]:
                dist += pg.Vector2(self.speed * dt, 0)
            if keys[K_UP]:
                dist += pg.Vector2(0, -self.speed * dt)
            if keys[K_DOWN]:
                dist += pg.Vector2(0, self.speed * dt)

            if not dist.x == 0 and not dist.y == 0:
                dist /= math.sqrt(2)

        else:
            if keys[K_LEFT]:
                dist += pg.Vector2(-self.speed * dt, 0)
            if keys[K_RIGHT]:
                dist += pg.Vector2(self.speed * dt, 0)

        if not dist == pg.Vector2(0, 0):
            self.move(dist)

    @Event.trigger(Events.PLAYER_MOVE)
    def move(self, dist):
        super().move(dist)

    def update(self):
        self.walk()

        super().update()

        # check if room transition
        for trans in Level.get_instance().get_room_transitions_valid():
            if self.collider.collide(trans.collider):
                print("transition to room:", trans.target_room, "with transition:", trans.target_transition_id)

                try:
                    Engine.import_room(trans.target_room)
                except FileNotFoundError:
                    raise FileNotFoundError("No such room: " + trans.target_room)

                for trans_target in Level.get_instance().get_room_transitions():
                    if trans_target.transition_id == trans.target_transition_id:
                        trans_target.set_cd(True)

                        self.change_pos(trans_target.pos + trans_target.player_spawn_offset())
                        break
                else:
                    raise RuntimeError("No transition found with ID: " + str(trans.target_transition_id) + " in room: " + trans.target_room)

    @classmethod
    def get_instance(cls):
        return cls._instance
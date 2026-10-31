import pygame as pg

import src.config as c


class Level:
    _instance = None

    def __init__(self):
        if Level._instance is not None:
            raise RuntimeError("Level already exists - use Level.get_instance() instead")
        self.layer_background = []
        self.layer_level = []
        self.layer_level_entity = []
        self.layer_entity = []
        self.layer_overlay = []

        self.s_layer_overlay = pg.Surface((c.WIDTH, c.HEIGHT), pg.SRCALPHA, 32).convert_alpha()

        Level._instance = self

    def get_layer_background(self):
        return self.layer_background

    def get_layer_level(self):
        return self.layer_level

    def get_layer_level_colliding(self):
        return [obj for obj in self.get_layer_level() if obj.is_colliding()]

    def get_layer_level_entity_colliding(self):
        return [obj for obj in self.get_layer_level_entity() if obj.is_colliding()]

    def get_layer_level_solid(self):
        return [obj for obj in self.get_layer_level_colliding() if obj.collider.is_solid]

    def get_layer_level_entity_solid(self):
        return [obj for obj in self.get_layer_level_entity_colliding() if obj.collider.is_solid]

    def get_room_transitions(self):
        return [obj for obj in self.get_layer_level_entity() if obj.create_name() == "room_transition"]

    def get_room_transitions_valid(self):
        return [obj for obj in self.get_layer_level_entity() if type(obj).__name__ == "RoomTransition" and not obj.on_cd]

    def get_player_spawner(self, spawner_id):
        return [obj for obj in self.get_layer_level() if type(obj).__name__ == "PlayerSpawner" and obj.spawner_id == spawner_id]

    def get_camara_cutoff(self):
        return [obj for obj in self.get_layer_level() if type(obj).__name__ == "CameraCutoff"]

    def get_solid(self):
        return self.get_layer_level_solid() + self.get_layer_level_entity_solid()

    def get_layer_level_entity(self):
        return self.layer_level_entity

    def get_layer_entity(self):
        return self.layer_entity

    def get_layer_entity_playerless(self):
        return [obj for obj in self.get_layer_entity() if not type(obj).__name__ == "PlayerEntity"]

    def get_layer_overlay(self):
        return self.layer_overlay

    def add_background(self, obj):
        self.layer_background.append(obj)

    def add_level(self, obj):
        self.layer_level.append(obj)

    def add_level_entity(self, obj):
        self.layer_level_entity.append(obj)

    def add_entity(self, obj):
        self.layer_entity.append(obj)

    def add_overlay(self, obj):
        self.layer_overlay.append(obj)

    def cleanse_level(self):
        self.layer_level = []

    def cleanse_entity_playerless(self):
        from entity.concrete.player.player_entity import PlayerEntity
        self.layer_entity = [PlayerEntity.get_instance()]

    def cleanse_level_entity(self):
        self.layer_level_entity = []

    def cleanse_background(self):
        self.layer_background = []

    @classmethod
    def get_instance(cls):
        return cls._instance
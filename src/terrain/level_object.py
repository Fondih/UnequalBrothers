from abc import ABC, abstractmethod
from json import JSONEncoder

import pygame as pg

from collider.collider import Collider
from event_handler.event_handler import Event
from event_handler.events import Events


class LevelObject(ABC):
    _texture = None

    def __init__(self, pos, scaler, rot):
        self.pos = pos
        self.scaler = scaler
        self.rot = rot
        cls = type(self)
        if cls._texture is None:
            cls._texture = self.create_texture()

        self.image = self.create_image()
        self.collider = self.create_collider()

    @classmethod
    def get_type(cls):
        return cls.__name__

    @classmethod
    def get_texture(cls):
        return cls._texture

    @classmethod
    def is_anim(cls):
        return False

    @classmethod
    def get_anim_frames(cls):
        return 1

    @classmethod
    def is_colliding(cls):
        return True

    @classmethod
    @abstractmethod
    def create_name(cls):
        return "level_object"

    @classmethod
    def create_namespace(cls):
        return ""

    @classmethod
    @abstractmethod
    def create_texture_size(cls):
        return 1, 1

    @classmethod
    def get_texture_size_scaled(cls, scaler):
        x, y = cls.create_texture_size()

        return x * scaler, y * scaler

    @classmethod
    def create_colorkey_custom(cls):
        return "black"

    @classmethod
    def create_texture(cls, name_custom=None, namespace_custom=None, colorkey_custom=None):
        if colorkey_custom is None:
            colorkey_custom = cls.create_colorkey_custom()
        if namespace_custom is None:
            namespace_custom = cls.create_namespace()
        if name_custom is None:
            name_custom = cls.create_name()

        name_custom = namespace_custom + name_custom

        try:
            img = pg.image.load("assets/textures/" + name_custom + ".png").convert_alpha()
            img.set_colorkey(colorkey_custom)

            return img
        except FileNotFoundError:
            print("\033[31m" + "Cannot load image: " + name_custom + " from: " + "assets/textures/" + name_custom + ".png" + "\033[0m")

            return pg.image.load("assets/textures/missing_texture.png").convert()

    def create_image(self):
        img = self.get_texture()
        img = pg.transform.scale(img, self.create_texture_size())
        img = pg.transform.scale_by(img, self.scaler)
        img = pg.transform.rotate(img, self.rot)

        return img

    @abstractmethod
    def create_collider(self):
        pass

    @classmethod
    def create_pos_offset(cls, scaler):
        return pg.Vector2(0, 0)

    def update(self):
        pass

    @abstractmethod
    def render(self, layer):
        pass

    @classmethod
    def scrap_texture(cls):
        cls._texture = None

class EncodeLevelObject(JSONEncoder):
    def default(self, o):
        if o.get_type() == "RoomTransition":
            return self.default_room_transition(o)
        if o.get_type() == "PlayerSpawner":
            return self.default_player_spawner(o)

        level_obj_dict = {
            "type": o.get_type(),
            "pos": o.pos.tuple(),
            "scaler": o.scaler,
            "rot": o.rot
        }

        return level_obj_dict

    @staticmethod
    def default_room_transition(o):
        level_obj_dict = {
            "type": o.get_type(),
            "pos": o.pos.tuple(),
            "scaler": o.scaler,
            "rot": o.rot,
            "target_room": o.target_room,
            "target_transition_id": o.target_transition_id,
            "transition_id": o.transition_id
        }

        return level_obj_dict

    @staticmethod
    def default_player_spawner(o):
        level_obj_dict = {
            "type": o.get_type(),
            "pos": o.pos.tuple(),
            "scaler": o.scaler,
            "rot": o.rot,
            "spawner_id": o.spawner_id,
        }

        return level_obj_dict
from abc import ABC, abstractmethod
from json import JSONEncoder
import pygame as pg
from collider.collider import Collider
from collider.colliders.rect_collider import RectCollider
from level.camera import Camera


# TODO: Save one Surface per level object image if possible instead of one per instance
class LevelObject(ABC):
    _texture = None

    def __init__(self, pos, scaler, rot, solid):
        self.pos = pos
        self.scaler = scaler
        self.rot = rot
        self.size = self.create_texture_size()
        self.solid = solid
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
    def has_alpha(cls):
        return False

    @classmethod
    def colorkey(cls):
        return None

    @classmethod
    def is_anim(cls):
        return False

    @classmethod
    def get_anim_frames(cls):
        return 1

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

    def change_size(self, size):
        self.size = size
        self.image = self.create_image()
        self.collider = self.create_collider()

    def get_texture_size_scaled(self, scaler):
        x, y = self.size

        return x * scaler, y * scaler

    @classmethod
    def create_texture(cls, name_custom=None, namespace_custom=None, colorkey_custom=None):
        if colorkey_custom is None: colorkey_custom = cls.colorkey()
        if namespace_custom is None: namespace_custom = cls.create_namespace()
        if name_custom is None: name_custom = cls.create_name()

        name_custom = namespace_custom + name_custom

        try:
            return pg.image.load("assets/textures/" + name_custom + ".png")
        except FileNotFoundError:
            print("\033[31m" + "Cannot load image: " + name_custom + " from: " + "assets/textures/" + name_custom + ".png" + "\033[0m")

            return pg.image.load("assets/textures/missing_texture.png").convert()

    def render(self, screen, cam, zoom):
        img = self.image
        if img is None:
            return
        cs_x, cs_y = cam.size
        off = self.create_pos_offset(self.scaler)
        x = (self.pos.x + off.x - cam.pos.x) * zoom + cs_x / 2
        y = (self.pos.y + off.y - cam.pos.y) * zoom + cs_y / 2
        if x > cs_x or y > cs_y or x + img.get_width() < 0 or y + img.get_height() < 0:
            return
        screen.blit(img, (x, y))

    def create_image(self):
        img = self.get_texture()

        sx, sy = self.size
        sx *= self.scaler * Camera.zoom()
        sy *= self.scaler * Camera.zoom()

        img = pg.transform.scale(img, (sx, sy))
        if not self.rot == 0:
            img = pg.transform.rotate(img, self.rot)

        if self.has_alpha():
            image = img.convert_alpha()
            image.set_colorkey(self.colorkey())
        else: image = img.convert()
        self.image = image
        return image

    def create_collider(self):
        return RectCollider(self.pos, self.get_texture_size_scaled(self.scaler), Collider.Type.LEVEL, is_solid=self.solid)

    @classmethod
    def create_pos_offset(cls, scaler):
        return pg.Vector2(0, 0)

    def update(self):
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
            "size": o.size,
            "rot": o.rot
        }

        return level_obj_dict

    @staticmethod
    def default_room_transition(o):
        level_obj_dict = {
            "type": o.get_type(),
            "pos": o.pos.tuple(),
            "scaler": o.scaler,
            "size": o.size,
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
            "size": o.size,
            "rot": o.rot,
            "spawner_id": o.spawner_id,
        }

        return level_obj_dict
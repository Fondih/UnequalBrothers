from abc import ABC, abstractmethod

import pygame as pg


class ScreenObject(ABC):
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
    def get_texture(cls):
        return cls._texture

    @classmethod
    def is_anim(cls):
        return False

    @classmethod
    def get_anim_frames(cls):
        return 1

    @classmethod
    @abstractmethod
    def create_name(cls):
        return "screen_object"

    @classmethod
    def create_namespace(cls):
        return ""

    @classmethod
    @abstractmethod
    def create_texture_size(cls):
        return 1, 1

    def get_texture_size_scaled(self):
        x, y = self.create_texture_size()

        return x * self.scaler, y * self.scaler

    def create_texture(self, colorkey_custom="black"):
        try:
            img = pg.image.load("assets/textures/overlay/" + self.create_namespace() + self.create_name() + ".png").convert_alpha()
            img.set_colorkey(colorkey_custom)

            return img
        except FileNotFoundError:
            print("\033[31m" + "Cannot load image:" + self.create_namespace() + self.create_name() + "\033[0m")

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

    def change_pos(self, pos):
        self.pos = pos
        self.collider.update_pos(pos)

    def update(self):
        pass

    @abstractmethod
    def render(self, layer):
        pass
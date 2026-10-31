from abc import ABC

import pygame as pg

import src.config as c
from collider.collider import Collider
from overlay.screen_object import ScreenObject


class Text(ScreenObject, ABC):
    _font_cache = {}

    def __init__(self, text, col, pos, size, scaler=1, rot=0, font_name=c.FONT_DEFAULT):
        self.text = text
        self.col = col
        self.size = size
        self.scaler = scaler
        self.size_font = self.create_font_size()
        self.font_name = font_name
        super().__init__(pos, scaler, rot)

    @classmethod
    def create_name(cls):
        return "text"

    def create_texture_size(self):
        return self.size

    def create_font_size(self):
        x, y = self.size

        return int(y * self.scaler)

    def create_collider(self):
        return Collider(self.pos, Collider.Type.MOUSE, is_solid=False)  # to avoid bugs if something checks colliders of all ScreenObjects

    def create_texture(self, colorkey_custom="black"):
        return None

    def render(self, layer):
        layer.blit(self.image, self.pos.tuple())

    def create_image(self):
        img = self.get_font().render(self.text, 1, self.col)
        img = pg.transform.scale_by(img, self.scaler)
        img = pg.transform.rotate(img, self.rot)

        return img

    def get_font(self):
        key = (self.font_name, self.size_font)
        if key not in Text._font_cache:
            Text._font_cache[key] = pg.font.SysFont(self.font_name, self.size_font)
        return Text._font_cache[key]
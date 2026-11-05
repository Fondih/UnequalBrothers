from abc import ABC

import pygame as pg

from collider.collider import Collider
from overlay.screen_object import ScreenObject


class Button(ScreenObject, ABC):
    def __init__(self, pos, scaler=1, rot=0):
        super().__init__(pos, scaler, rot)

        self.on_cooldown = False

    @classmethod
    def create_name(cls):
        return "button"

    def set_on_cooldown(self, cd):
        self.on_cooldown = cd

    def create_collider(self):
        return Collider(self.pos, Collider.Type.MOUSE, is_solid=False)

    def render(self, layer, cam):
        layer.blit(self.image, self.pos.tuple())

    @staticmethod
    def clicked():
        pass

    def update(self):
        if self.collider.collide(pg.mouse.get_pos()):
            if not self.on_cooldown:
                self.clicked()
        if self.collider.button_held():
            self.on_cooldown = True
        else:
            self.on_cooldown = False
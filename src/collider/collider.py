from enum import Enum, auto

import pygame as pg


class Collider:
    class Type(Enum):
        LEVEL = auto()
        MOUSE = auto()

    def __init__(self, pos, collider_type, is_solid=True, buttons_mouse=None, requires_clicking=True):
        self.buttons_mouse = buttons_mouse
        if buttons_mouse is None:
            self.buttons_mouse = [0]
        self.requires_clicking = requires_clicking

        self.pos = pos
        self.type = collider_type
        self.is_solid = is_solid

    def get_distance(self, other, direction):
        return pg.Vector2(0, 0)

    def collide(self, other, overwrite_type=False, overwrite_buttons=None):
        return False

    def update(self, pos, _=None):
        self.pos = pos

    def rotate(self, rot):
        pass

    def button_held(self, overwrite_type=False, overwrite_buttons=None):
        if overwrite_buttons is None:
            overwrite_buttons = self.buttons_mouse
        if self.type == Collider.Type.MOUSE or overwrite_type:
            for b in overwrite_buttons:
                if pg.mouse.get_pressed()[b]:
                    return True
        return False
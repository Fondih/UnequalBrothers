from abc import ABC

import pygame as pg

import src.config as c
from datatype.coordinate import Coordinate
from engine import Engine
from level.camera import Camera
from overlay.menu import Menu
from overlay.sided_screen_object import SidedScreenObject


class GridVisualMenu(Menu, SidedScreenObject, ABC):
    def __init__(self, pos, side):
        super().__init__(pos)
        self.side = side

    @classmethod
    def create_name(cls):
        return "grid_visual_menu"

    @classmethod
    def grid_color(cls):
        return "black"

    @classmethod
    def grid_line_width(cls):
        return 1

    def create_texture(self, colorkey_custom="black"):
        surface = pg.Surface(self.get_texture_size_scaled(), pg.SRCALPHA, 32).convert_alpha()

        surface = surface.convert_alpha()
        surface.set_colorkey(colorkey_custom)

        for i in range(0, c.WIDTH // c.GRID_SIZE + 2):
            x = c.GRID_SIZE * i

            pg.draw.line(surface, self.grid_color(), (x, 0), (x, c.HEIGHT + c.GRID_SIZE), self.grid_line_width())

        for i in range(0, c.HEIGHT // c.GRID_SIZE + 2):
            y = c.GRID_SIZE * i

            pg.draw.line(surface, self.grid_color(), (0, y), (c.WIDTH + c.GRID_SIZE, y), self.grid_line_width())

        return surface

    def render(self, surface, _):
        if not self.shown:
            return
        cam = Engine.inst().cams[{"left": "big", "right": "small"}.get(self.side, "full")]
        w, h = surface.get_size()
        z = Camera.zoom()
        step = c.GRID_SIZE * z
        ox = (-(cam.pos.x * z) + w / 2) % step
        oy = (-(cam.pos.y * z) + h / 2) % step
        x = ox
        while x < w:
            pg.draw.line(surface, self.grid_color(), (x, 0), (x, h), self.grid_line_width())
            x += step
        y = oy
        while y < h:
            pg.draw.line(surface, self.grid_color(), (0, y), (w, y), self.grid_line_width())
            y += step

    @classmethod
    def create_texture_size(cls):
        return c.WIDTH + c.GRID_SIZE, c.HEIGHT + c.GRID_SIZE

    def create_content(self):
        return []
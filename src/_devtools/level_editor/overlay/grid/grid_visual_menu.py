from abc import ABC

import pygame as pg

import src.config as c
from datatype.coordinate import Coordinate
from level.camera import Camera
from overlay.menu import Menu


class GridVisualMenu(Menu, ABC):
    def __init__(self, pos):
        super().__init__(pos)

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


    def render(self, layer):
        if self.shown:
            x, y = (Camera.get_instance().pos + pg.Vector2(-c.WIDTH // 2, -c.HEIGHT // 2)).tuple()
            x -= x % c.GRID_SIZE
            y -= y % c.GRID_SIZE

            pos = Coordinate(x, y).convert_to_surface().tuple()

            layer.blit(self.image, pos)

    @classmethod
    def create_texture_size(cls):
        return c.WIDTH + c.GRID_SIZE, c.HEIGHT + c.GRID_SIZE

    def create_content(self):
        return []
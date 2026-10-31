import pygame as pg

import config as c
from event_handler.event_handler import Event
from event_handler.events import Events


class Camera:
    _instance = None

    def __init__(self, pos, zoom=1):
        if Camera._instance is not None:
            raise RuntimeError("Camera already exists - use Camera.get_instance() instead")

        self.pos = pos  # center in middle of camera
        self.zoom = zoom
        Camera._instance = self

    @Event.trigger(Events.ZOOM_CHANGE)
    def change_zoom(self, zoom):
        self.zoom = zoom

    def set_pos(self, pos):
        self.pos = self.border_cam(pos)

    @classmethod
    def get_instance(cls):
        return cls._instance

    def world_to_layer(self, world_pos):
        return world_pos * self.zoom

    def layer_offset1(self):
        return pg.Vector2(c.WIDTH / 2, c.HEIGHT / 2) - pg.Vector2((self.pos * self.zoom).tuple())

    def border_cam(self, pos):
        from datatype.coordinate import Coordinate
        from level.level import Level

        borders = Level.get_instance().get_camara_cutoff()
        if len(borders) == 0:
            return pos

        border = borders[0]
        bs_x, bs_y = border.size

        x, y = pos.tuple()

        if bs_x >= c.WIDTH / self.zoom:
            if pos.x - c.WIDTH / self.zoom / 2 < border.pos.x:
                x = border.pos.x + c.WIDTH / self.zoom / 2
            elif pos.x + c.WIDTH / self.zoom / 2 > border.pos.x + bs_x:
                x = border.pos.x + bs_x - c.WIDTH / self.zoom / 2
        if bs_y >= c.HEIGHT / self.zoom:
            if pos.y - c.HEIGHT / self.zoom / 2 < border.pos.y:
                y = border.pos.y + c.HEIGHT / self.zoom / 2
            elif pos.y + c.HEIGHT / self.zoom / 2 > border.pos.y + bs_y:
                y = border.pos.y + bs_y - c.HEIGHT / self.zoom / 2

        return Coordinate(x, y)
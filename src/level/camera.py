import pygame as pg

import config as c
from event_handler.event_handler import Event
from event_handler.events import Events


class Camera:
    _zoom = 1
    
    def __init__(self, pos, size):
        self.pos = pos  # center in middle of camera
        self.size = size

    @classmethod
    def zoom(cls):
        return cls._zoom
    
    @classmethod
    @Event.trigger(Events.ZOOM_CHANGE)
    def set_zoom(cls, zoom):
        cls._zoom = zoom

    def set_pos(self, pos):
        self.pos = self.border_cam(pos)

    def border_cam(self, pos):
        from datatype.coordinate import Coordinate
        from level.level import Level

        borders = Level.inst().get_camara_cutoff()
        if len(borders) == 0:
            return pos

        border = borders[0]
        bs_x, bs_y = border.size
        s_x, s_y = self.size

        x, y = pos.tuple()

        if bs_x >= s_x / self.zoom():
            if pos.x - s_x / self.zoom() / 2 < border.pos.x:
                x = border.pos.x + s_x / self.zoom() / 2
            elif pos.x + s_x / self.zoom() / 2 > border.pos.x + bs_x:
                x = border.pos.x + bs_x - s_x / self.zoom() / 2
        if bs_y >= s_y / self.zoom():
            if pos.y - s_y / self.zoom() / 2 < border.pos.y:
                y = border.pos.y + s_y / self.zoom() / 2
            elif pos.y + s_y / self.zoom() / 2 > border.pos.y + bs_y:
                y = border.pos.y + bs_y - s_y / self.zoom() / 2

        return Coordinate(x, y)
import pygame as pg


class SidedScreenObject:
    def __init__(self, *args, side=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.side = side

    def calc_pos_offset(self, pos, cam):
        if self.side == "right":
            cs_x, _ = cam.size
            pos += pg.Vector2(cs_x, 0)
        return pos
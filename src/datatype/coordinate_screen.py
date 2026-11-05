import pygame as pg
import config as c


class CoordinateScreen:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        try:
            return CoordinateScreen(self.x + other.x, self.y + other.y)
        except TypeError:
            raise TypeError(f"Cannot add {type(other)} to {type(self)}")

    def __sub__(self, other):
        try:
            return CoordinateScreen(self.x - other.x, self.y - other.y)
        except TypeError:
            raise TypeError(f"Cannot subtract {type(other)} from {type(self)}")

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            return CoordinateScreen(self.x * other, self.y * other)
        else:
            try:
                return CoordinateScreen(self.x * other.x, self.y * other.y)

            except TypeError:
                raise TypeError(f"Cannot multiply {type(self)} with {type(other)}")

    def __truediv__(self, other):
        if isinstance(other, (float, int)):
            return CoordinateScreen(self.x / other, self.y / other)
        try:
            return CoordinateScreen(self.x / other.x, self.y / other.y)
        except TypeError:
            raise TypeError(f"Cannot divide {type(self)} by {type(other)}")

    def __floordiv__(self, other):
        if isinstance(other, (float, int)):
            return CoordinateScreen(self.x // other, self.y // other)
        try:
            return CoordinateScreen(self.x // other.x, self.y // other.y)
        except TypeError:
            raise TypeError(f"Cannot floordivide {type(self)} by {type(other)}")

    def __abs__(self):
        return CoordinateScreen(abs(self.x), abs(self.y))

    def __eq__(self, other):
        return all([type(self) is type(other), self.x == other.x, self.y == other.y])

    def pos(self):
        return pg.Vector2(self.x, self.y)

    def tuple(self):
        return self.x, self.y

    def convert_to_world(self, cam):
        from src.datatype.coordinate import Coordinate

        cs_x, cs_y = cam.size
        x = self.x + cam.pos.x - cs_x // 2
        y = self.y + cam.pos.y - cs_y // 2

        return Coordinate(int(x), int(y))
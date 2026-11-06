import pygame as pg

from collider.collider import Collider


class RectCollider(Collider):
    def __init__(self, pos, size, type_collider, is_solid=True, buttons_mouse=None, requires_clicking=True):
        super().__init__(pos, type_collider, is_solid=is_solid, buttons_mouse=buttons_mouse,
                         requires_clicking=requires_clicking)

        self.size = size
        self.rect = self.create_rect()
        self.probe = self.create_probe()

    def create_rect(self):
        return pg.Rect(self.pos.tuple(), self.size)

    def create_probe(self):
        if self.type == Collider.Type.LEVEL:
            return RectColliderProbe(self.pos, self.size)
        return None

    def get_distance(self, other, direction):
        if isinstance(other, RectCollider):
            x, y = (0, 0)
            ss_x, ss_y = self.size
            os_x, os_y = other.size

            if direction == 0:
                if self.pos.x <= other.pos.x:
                    x = other.pos.x - self.pos.x - ss_x
                else:
                    x = other.pos.x - self.pos.x + os_x
            elif direction == 1:
                if self.pos.y <= other.pos.y:
                    y = other.pos.y - self.pos.y - ss_y
                else:
                    y = other.pos.y - self.pos.y + os_y

            return pg.Vector2(x, y)
        else:
            super().collide(other)

    def collide(self, other, overwrite_type=False, overwrite_buttons=None):
        if (self.type == Collider.Type.LEVEL or overwrite_type) and isinstance(other, RectCollider):
            return self.rect.colliderect(other.rect)
        elif (self.type == Collider.Type.MOUSE or overwrite_type) and isinstance(other, tuple):
            if overwrite_buttons is None:
                overwrite_buttons = self.buttons_mouse

            if not self.requires_clicking or self.button_held(True, overwrite_buttons):
                return self.rect.collidepoint(other)
        else:
            return super().collide(other)

    def cprobe(self, dpos):
        self.probe.update(self.pos + dpos, self.size)
        return self.probe

    def update(self, pos, size=None):
        if size is None: size = self.size
        super().update(pos, size)
        self.size = size
        self.rect.update(self.pos.tuple(), self.size)


class RectColliderProbe(Collider):
    def __init__(self, pos, size):
        super().__init__(pos, Collider.Type.LEVEL)

        self.size = size
        self.rect = self.create_rect()

    def create_rect(self):
        return pg.Rect(self.pos.tuple(), self.size)

    def collide(self, other, overwrite_type=False, overwrite_buttons=None):
        if isinstance(other, RectCollider):
            return self.rect.colliderect(other.rect)
        else:
            return super().collide(other)

    def update(self, pos, size=None):
        if size is None: size = self.size
        super().update(pos, size)
        self.size = size
        self.rect.update(self.pos.tuple(), self.size)
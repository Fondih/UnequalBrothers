import pygame as pg
from collider.collider import Collider


class RectCollider(Collider):
    def __init__(self, pos, size, type_collider, is_solid=True, buttons_mouse=None, requires_clicking=True):
        super().__init__(pos, type_collider, is_solid=is_solid, buttons_mouse=buttons_mouse, requires_clicking=requires_clicking)

        self.size = size
        self.rect = self.create_rect()

    def create_rect(self):
        return pg.Rect(self.pos.tuple(), self.size)

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

    def collide(self, other):
        if self.type == Collider.Type.LEVEL and isinstance(other, RectCollider):
            return self.rect.colliderect(other.rect)
        elif self.type == Collider.Type.MOUSE and isinstance(other, tuple):
            if not self.requires_clicking or self.button_held():
                return self.rect.collidepoint(other)
        else:
            return super().collide(other)

    def create_moved_copy(self, dist):
        return RectCollider(self.pos + dist, self.size, self.type, self.is_solid)

    def update_pos(self, pos):
        super().update_pos(pos)

        self.rect = self.create_rect()
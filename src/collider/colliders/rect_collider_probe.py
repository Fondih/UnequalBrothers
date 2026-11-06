import pygame as pg
from collider.collider import Collider


class RectColliderProbe(Collider):
    def __init__(self, pos, size):
        super().__init__(pos, Collider.Type.LEVEL)

        self.size = size
        self.rect = self.create_rect()

    def create_rect(self):
        return pg.Rect(self.pos.tuple(), self.size)

    def collide(self, other, overwrite_type=False, overwrite_buttons=None):
        from collider.colliders.rect_collider import RectCollider


        if isinstance(other, RectCollider):
            return self.rect.colliderect(other.rect)
        else:
            return super().collide(other)

    def update(self, pos, size):
        super().update(pos, size)
        self.size = size
        self.rect.update(self.pos.tuple(), self.size)
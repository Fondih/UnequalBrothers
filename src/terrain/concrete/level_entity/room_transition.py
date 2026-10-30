from abc import ABC

import pygame as pg

from _devtools.level_editor.overlay.editor_terrain_menu.menu_type_registry import spec_menu
from _devtools.level_editor.overlay.editor_terrain_menu.menus import Menus
from collider.collider import Collider
from collider.colliders.rect_collider import RectCollider
from terrain.level_entity import LevelEntity
from terrain.terrain_registry import register


@register(["level utils"])
class RoomTransition(LevelEntity, ABC):
    def __init__(self, pos, target_room: str, target_transition_id: int, transition_id: int, scaler=1, rot=0):
        super().__init__(pos, scaler=scaler, rot=rot)

        self.target_room = target_room
        self.target_transition_id = target_transition_id
        self.transition_id = transition_id
        self.on_cd = False

    @classmethod
    def create_name(cls):
        return "room_transition"

    @classmethod
    def create_texture_size(cls):
        return 50, 100

    def set_cd(self, cd):
        self.on_cd = cd

    def player_spawn_offset(self):
        x, y = self.create_texture_size()

        return pg.Vector2(x // 2, y) * self.scaler

    def create_collider(self):
        return RectCollider(self.pos, self.get_texture_size_scaled(self.scaler), Collider.Type.LEVEL, is_solid=False)

    def update(self):
        from entity.concrete.player.player_entity import PlayerEntity

        super().update()

        if self.on_cd and not self.collider.collide(PlayerEntity.get_instance().collider):
            self.set_cd(False)
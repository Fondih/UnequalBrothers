from abc import ABC

import pygame as pg

from _devtools.level_editor.overlay.editor_terrain_menu.menu_type_registry import spec_menu
from _devtools.level_editor.overlay.editor_terrain_menu.menus import Menus
from engine import Engine
from level.level import Level
from terrain.terrain import Terrain
from terrain.terrain_registry import register


@spec_menu(Menus.RESIZABLE_RECT)
@register(["level utils"])
class RoomTransition(Terrain, ABC):
    def __init__(self, pos, target_room: str, target_transition_id: int, transition_id: int, scaler=1, rot=0):
        super().__init__(pos, scaler=scaler, rot=rot, solid=False)

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
        x, y = self.size

        return pg.Vector2(x // 2, y // 2) * self.scaler

    def update(self):
        from player.player_big import PlayerBig
        from player.player_small import PlayerSmall

        super().update()

        # check for player collision
        if (not self.on_cd and self.collider.collide(PlayerSmall.inst().collider)
                and self.collider.collide(PlayerBig.inst().collider)):
            print("transition to room:", self.target_room, "with transition:", self.target_transition_id)

            try:
                Engine.import_room(self.target_room)
            except FileNotFoundError:
                raise FileNotFoundError("No such room: " + self.target_room)

            for trans_target in Level.inst().get_room_transitions():
                if trans_target.transition_id == self.target_transition_id:
                    trans_target.set_cd(True)

                    PlayerBig.inst().change_pos(trans_target.pos + trans_target.player_spawn_offset())
                    PlayerSmall.inst().change_pos(trans_target.pos + trans_target.player_spawn_offset())
                    break
            else:
                raise RuntimeError(
                    "No transition found with ID: " + str(self.target_transition_id) + " in room: " + self.target_room)

        # check for cd reset
        if (self.on_cd and not self.collider.collide(PlayerSmall.inst().collider)
                and not self.collider.collide(PlayerBig.inst().collider)):
            self.set_cd(False)
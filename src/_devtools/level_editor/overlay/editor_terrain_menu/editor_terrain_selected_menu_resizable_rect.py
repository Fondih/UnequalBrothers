import pygame as pg

from _devtools.level_editor.overlay.editor_terrain_menu.editor_terrain_selected_commit_button import \
    EditorTerrainSelectedCommitButton
from _devtools.level_editor.overlay.editor_terrain_menu.editor_terrain_selected_delete_button import \
    EditorTerrainSelectedDeleteButton
from _devtools.level_editor.overlay.editor_terrain_menu.editor_terrain_selected_resize_rect_lever import \
    EditorTerrainSelectedResizeRectLever
from datatype.coordinate_screen import CoordinateScreen
from overlay.menu import Menu


class EditorTerrainSelectedMenuResizeableRect(Menu):
    def __init__(self, pos):
        super().__init__(pos)

        self.set_shown(True)

    @classmethod
    def create_name(cls):
        return "editor_terrain_selected_menu_resizeable_rect"

    @classmethod
    def create_offset(cls):
        x, y = cls.create_texture_size()

        return pg.Vector2(-x // 2, -y - 7)

    def create_texture(self, colorkey_custom="black"):
        texture = pg.Surface(self.get_texture_size_scaled(), pg.SRCALPHA, 32)
        texture.convert_alpha()
        texture.fill((90, 90, 90, 100))

        return texture

    def create_content(self):
        return [EditorTerrainSelectedDeleteButton(CoordinateScreen(0, 0), pg.Vector2(65, 5)),
                EditorTerrainSelectedCommitButton(CoordinateScreen(0, 0), pg.Vector2(35, 5)),
                EditorTerrainSelectedResizeRectLever(CoordinateScreen(0, 0), pg.Vector2(5, 5))]

    @classmethod
    def create_texture_size(cls):
        return 95, 35

    def update(self):
        for obj in self.content:
            obj.change_pos(self.pos + obj.create_offset())

        super().update()
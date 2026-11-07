from abc import ABC

import config as c

from _devtools.level_editor.overlay.editing_menu.terrain_place_lever import TerrainPlaceLever
from _devtools.level_editor.overlay.grid.grid_visual_menu_lever import GridVisualMenuLever
from _devtools.level_editor.overlay.gui.editor_export_button import EditorExportButton
from _devtools.level_editor.overlay.gui.editor_room_new_button import EditorRoomNewButton
from _devtools.level_editor.overlay.gui.noclip_lever import NoclipLever
from _devtools.level_editor.overlay.gui.undo_commit_button import UndoCommitButton
from datatype.coordinate_screen import CoordinateScreen
from overlay.menu import Menu
from overlay.overlays.fps_display import FPSDisplay


class EditingGuiMenu(Menu, ABC):
    def __init__(self, pos):
        super().__init__(pos)

        self.shown = True

    @classmethod
    def create_name(cls):
        return "editing_gui_menu"

    def create_texture(self, colorkey_custom="black"):
        pass

    def create_image(self):
        pass

    @classmethod
    def create_texture_size(cls):
        return 0, 0

    def create_content(self):
        terrain_place_lever = TerrainPlaceLever(CoordinateScreen(c.WIDTH - 70, 20))

        return [terrain_place_lever,
                terrain_place_lever.menu,
                UndoCommitButton(CoordinateScreen(c.WIDTH - 110, 30)),
                GridVisualMenuLever(CoordinateScreen(c.WIDTH - 150, 30)),
                NoclipLever(CoordinateScreen(c.WIDTH - 190, 30)),
                EditorExportButton(CoordinateScreen(20, 20)),
                EditorRoomNewButton(CoordinateScreen(80, 20)),
                FPSDisplay()]
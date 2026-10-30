from enum import Enum

from _devtools.level_editor.overlay.editor_terrain_menu.editor_terrain_selected_menu_extended import \
    EditorTerrainSelectedMenuExtended
from _devtools.level_editor.overlay.editor_terrain_menu.editor_terrain_selected_menu_reduced import \
    EditorTerrainSelectedMenuDefault


class Menus(Enum):
    DEFAULT = EditorTerrainSelectedMenuDefault
    EXTENDED = EditorTerrainSelectedMenuExtended
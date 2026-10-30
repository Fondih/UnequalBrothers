from abc import ABC

from collider.collider import Collider
from collider.colliders.rect_collider import RectCollider
from overlay.button import Button


class EditorTerrainSelectedDeleteButton(Button, ABC):
    def __init__(self, pos, offset):
        super().__init__(pos)

        self.offset = offset

    @classmethod
    def create_name(cls):
        return "editor_terrain_selected_delete_button"

    @classmethod
    def create_texture_size(cls):
        return 25, 25

    def create_offset(self):
        return self.offset

    def create_collider(self):
        return RectCollider(self.pos, self.get_texture_size_scaled(), Collider.Type.MOUSE, is_solid=False)

    def clicked(self):
        from _devtools.level_editor.terrain.editor_terrain_selected import EditorTerrainSelected

        EditorTerrainSelected.get_instance().scrap()
from abc import ABC

from _devtools.level_editor.terrain.editor_terrain_selected import EditorTerrainSelected
from collider.collider import Collider
from collider.colliders.rect_collider import RectCollider
from overlay.lever import Lever


class EditorTerrainSelectedResizeRectLever(Lever, ABC):
    def __init__(self, pos, offset):
        super().__init__(pos)

        self.offset = offset

    @classmethod
    def create_name(cls):
        return "editor_terrain_selected_resize_rect_lever"

    @classmethod
    def create_texture_size(cls):
        return 25, 25

    def create_offset(self):
        return self.offset

    def create_collider(self):
        return RectCollider(self.pos, self.get_texture_size_scaled(), Collider.Type.MOUSE, is_solid=False)

    def clicked(self):
        super().clicked()
        EditorTerrainSelected.get_instance().set_resize(self.state)
from abc import ABC

from collider.collider import Collider
from collider.colliders.rect_collider import RectCollider
from overlay.button import Button


class UndoCommitButton(Button, ABC):
    def __init__(self, pos, scaler=1):
        super().__init__(pos, scaler=scaler)

    @classmethod
    def create_name(cls):
        return "undo_commit_button"

    @classmethod
    def create_texture_size(cls):
        return 30, 30

    def create_collider(self):
        return RectCollider(self.pos, self.get_texture_size_scaled(), Collider.Type.MOUSE, is_solid=False)

    def clicked(self):
        from _devtools.level_editor.terrain.editor_terrain_selected import EditorTerrainSelected

        EditorTerrainSelected.undo_commit()
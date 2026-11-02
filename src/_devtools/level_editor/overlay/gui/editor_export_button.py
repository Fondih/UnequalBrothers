from abc import ABC

from collider.collider import Collider
from collider.colliders.rect_collider import RectCollider
from engine import Engine
from overlay.button import Button


class EditorExportButton(Button, ABC):
    def __init__(self, pos, scaler=1):
        super().__init__(pos, scaler=scaler)

    @classmethod
    def create_name(cls):
        return "editor_export_button"

    @classmethod
    def create_texture_size(cls):
        return 40, 40

    def create_collider(self):
        return RectCollider(self.pos, self.get_texture_size_scaled(), Collider.Type.MOUSE, is_solid=False)

    def clicked(self):
        Engine.export_room()
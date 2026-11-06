from abc import ABC

from _devtools.level_editor.overlay.editor_terrain_menu import menu_type_registry
from _devtools.level_editor.overlay.editor_terrain_menu.menus import Menus
from collider.collider import Collider
from collider.colliders.rect_collider import RectCollider
from terrain.terrain import Terrain
from terrain.terrain_registry import register
from utils.tile_texture import tile_texture


@menu_type_registry.spec_menu(Menus.RESIZABLE_RECT)
@register(["wall"])
class WallStone(Terrain, ABC):
    def __init__(self, pos, scaler=1, rot=0):
        super().__init__(pos, scaler=scaler, rot=rot)

    @classmethod
    def create_name(cls):
        return "wall_stone"

    @classmethod
    def create_texture_size(cls):
        return 50, 50

    def create_image(self):
        img = self.get_texture()
        s_x, s_y = self.size
        ts_x, ts_y = self.create_texture_size()

        img = tile_texture(img, ts_x * self.scaler, ts_y * self.scaler, s_x, s_y)

        if self.has_alpha():
            image = img.convert_alpha()
            image.set_colorkey(self.colorkey())
        else: image = img.convert()
        self.image = image
        return image
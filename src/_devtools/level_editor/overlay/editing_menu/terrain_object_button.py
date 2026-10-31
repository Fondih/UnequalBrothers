from abc import ABC

import pygame as pg

from collider.collider import Collider
from collider.colliders.rect_collider import RectCollider
from datatype.coordinate_screen import CoordinateScreen
from entity.concrete.player.player_entity import PlayerEntity
from event_handler.event_handler import Event
from event_handler.events import Events
from level.level import Level
from overlay.button import Button
from overlay.text import Text


class TerrainObjectButton(Button, ABC):
    def __init__(self, pos, cls):
        self.content_class = cls
        self.texture = self.create_texture()
        super().__init__(pos, scaler=self.create_scaler())

    def get_size_y(self):
        x, y = self.get_texture_size_scaled()

        return y + 15

    def get_texture(self):
        return self.texture

    @classmethod
    def create_name(cls):
        return "terrain_object_button"

    def create_collider(self):
        return RectCollider(self.pos, self.get_texture_size_scaled(), Collider.Type.MOUSE, is_solid=False)

    def create_texture_size(self):
        return self.get_class().create_texture_size()

    def create_scaler(self):
        size_target_x = 50
        x, y = self.create_texture_size()
        return size_target_x / x

    def get_content_name(self):
        return self.content_class.create_name()

    def get_class(self):
        return self.content_class

    def create_texture(self, colorkey_custom="black"):
        return self.get_class().create_texture(name_custom=self.get_content_name(), colorkey_custom=colorkey_custom)



    """    def create_texture(self, colorkey_custom="black"):
        try:
            if not self.get_class().is_anim():
                img = pg.image.load("assets/textures/terrain/" +
                                    self.get_class().create_namespace() + self.get_content_name() + ".png").convert_alpha()
                img.set_colorkey(colorkey_custom)

                return img
            else:
                images = []
                for s in range(0, self.get_class().get_anim_frames()):
                    img = pg.image.load("assets/textures/overlay/" + self.get_class().create_namespace() +
                                        self.get_content_name() + "_" + str(s) + ".png").convert_alpha()
                    img.set_colorkey(colorkey_custom)
                    images.append(img)

                return images

        except FileNotFoundError:
            print("\033[31m" + "Cannot load image:" + self.get_class().create_namespace() + self.get_content_name() + "\033[0m")
            if not self.get_class().is_anim():
                return pg.image.load("assets/textures/missing_texture.png").convert()
            else:
                images = []
                for s in range(0, self.get_class().get_anim_frames()):
                    img = pg.image.load("assets/textures/missing_texture.png").convert()
                    images.append(img)

                return images
"""

    def create_image(self):
        if not self.get_class().is_anim():
            x, y = self.get_texture_size_scaled()
            height_text = 15
            img = super().create_image()

            name = self.get_content_name()
            text = Text(name, "black", CoordinateScreen(0, y), (x, height_text))

            surface = pg.Surface((x * 3, y + height_text * 5 / 3), pg.SRCALPHA, 32).convert_alpha()
            surface.blit(img, (0, 0))
            text.render(surface)

            return surface
        else:
            x, y = self.get_texture_size_scaled()
            height_text = 15
            name = self.get_content_name()
            text = Text(name, "black", CoordinateScreen(0, y), (x, height_text))
            images = []

            for s in range(0, self.get_class().get_anim_frames()):
                img = self.get_texture()[s]
                img = pg.transform.scale(img, self.create_texture_size())
                img = pg.transform.scale_by(img, self.scaler)
                img = pg.transform.rotate(img, self.rot)

                surface = pg.Surface((x * 3, y + height_text * 5 / 3), pg.SRCALPHA, 32).convert_alpha()
                surface.blit(img, (0, 0))
                text.render(surface)

                images.append(img)

            return images

    @Event.trigger(Events.EDITOR_TERRAIN_CREATED)
    def clicked(self):
        from _devtools.level_editor.terrain.editor_terrain_selected import EditorTerrainSelected

        if not EditorTerrainSelected.get_instance() is None:
            EditorTerrainSelected.get_instance().scrap()
        terrain = EditorTerrainSelected(self.get_class(), PlayerEntity.get_instance().pos)
        Level.get_instance().add_level_entity(terrain)

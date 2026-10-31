import pygame as pg
from overlay.menu import Menu
from overlay.text import Text


class EditorTerrainSelectedInfoMenu(Menu):
    _instance = None

    def __init__(self, pos, content_type):
        self.content_type = content_type
        EditorTerrainSelectedInfoMenu._instance = self  # temp as fix for bug if removed

        super().__init__(pos)

        self.set_shown(True)
        EditorTerrainSelectedInfoMenu._instance = self

    @classmethod
    def create_name(cls):
        return cls.getinstance().content_type.create_name()

    def create_image(self):
        img = self.get_texture()
        sx, sy = img.get_size()
        _, target_sy = self.create_texture_size()
        img = pg.transform.scale_by(img, target_sy / sy)

        self.image = img
        return img

    def create_texture(self, colorkey_custom="black"):
        return self.content_type.create_texture()

    def create_content(self):
        return [Text(self.create_name(), "black", self.pos - pg.Vector2(0, 40), (100, 20))]

    @classmethod
    def create_texture_size(cls):
        return 100, 100

    @staticmethod
    def getinstance():
        return EditorTerrainSelectedInfoMenu._instance

    def scrap(self):
        EditorTerrainSelectedInfoMenu._texture = None
        self.image = None
        EditorTerrainSelectedInfoMenu._instance = None
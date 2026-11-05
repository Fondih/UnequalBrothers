from abc import ABC

import pygame as pg

import src.config as c
from _devtools.level_editor.overlay.editing_menu.terrain_object_button import TerrainObjectButton
from collider.collider import Collider
from collider.colliders.rect_collider import RectCollider
from datatype.coordinate_screen import CoordinateScreen
from engine import Engine
from entity import entity_registry
from overlay.lever import Lever
from overlay.text import Text
from terrain import terrain_registry


class TerrainFolderLever(Lever, ABC):
    def __init__(self, pos, path, pos_root):
        self.pos_root = pos_root
        self.path = path
        self.content_structure = None
        self.content = None
        super().__init__(pos)

    @classmethod
    def create_name(cls):
        return "terrain_folder_lever"

    def create_collider(self):
        return RectCollider(self.pos, self.get_texture_size_scaled(), Collider.Type.MOUSE, is_solid=False)

    @classmethod
    def create_texture_size(cls):
        return 20, 20

    def get_content(self):
        if self.content is None:
            self.content = self.create_content()
        return self.content

    def get_folder_name(self):
        return self.path[-1]

    def get_size_y_extended(self):
        if self.state == 0:
            return self.get_texture_size_scaled()[1]

        bottom = self.pos.y + self.get_texture_size_scaled()[1]
        for cnt in self.get_content():
            if isinstance(cnt, TerrainFolderLever):
                h = cnt.get_size_y_extended()
            else:
                h = cnt.get_size_y()
            bottom = max(bottom, cnt.pos.y + h)
        return bottom - self.pos.y

    def create_content(self):
        content = []
        registry = {}

        match self.path[0]:
            case "terrain":
                registry = terrain_registry.get_all()
            case "entity":
                registry = entity_registry.get_all()

        def pathcheck(item):
            n, (_, g) = item

            if self.path == g[0:len(self.path)]:
                return True
            return False


        items = list(filter(pathcheck, registry.items()))

        levers = []

        for name, e in items:
            cls, group = e

            if len(group) > len(self.path):
                if group not in levers:
                    lever = TerrainFolderLever(CoordinateScreen(0, 0),
                                               group[0:len(self.path) + 1], self.pos_root)
                    content.append(lever)
                    levers.append(group)
            else:
                button = TerrainObjectButton(CoordinateScreen(0, 0), cls)
                content.append(button)
        return content

    def update(self, folder_parent=None, folder_above=None):
        super().update()

        if folder_parent is None:
            self.change_pos(self.pos_root)
        else:
            if folder_above is None:
                s_x, s_y = self.get_texture_size_scaled()

                self.change_pos(folder_parent.pos + pg.Vector2(7, s_y + 3))
            else:
                s_y = folder_above.get_size_y_extended()

                self.change_pos(folder_above.pos + pg.Vector2(0, s_y + 15))

        if self.state == 1:
            folder_above_next = None
            folders_count = 0

            folders = []
            terrains = []

            for cnt in self.get_content():
                if isinstance(cnt, TerrainFolderLever):
                    folders.append(cnt)
                else:
                    terrains.append(cnt)

            for f in folders:
                f.update(folder_parent=self, folder_above=folder_above_next)
                folder_above_next = f
                folders_count += 1
            if folder_above_next is not None:
                y = folder_above_next.pos.y + folder_above_next.get_size_y_extended() + 3
            else:
                y = self.pos.y + self.get_texture_size_scaled()[1] + 3

            for t in terrains:
                t.update()
                t.change_pos(CoordinateScreen(self.pos.x + 10, y))
                y += t.get_size_y() + 10

    def create_image(self):
        s_x, s_y = self.get_texture_size_scaled()

        images = super().create_image()
        text = Text(self.get_folder_name(), "black",
                    CoordinateScreen(s_x + 5, -4), (c.WIDTH // 2, s_y))
        fused = []

        for img in images:
            surface = pg.Surface((c.WIDTH // 2, int(s_y * 5 / 3)), pg.SRCALPHA, 32).convert_alpha()
            surface.blit(img, (0, 0))
            text.render(surface, Engine.inst().cams["full"])
            fused.append(surface)
        return fused


    def render(self, layer, cam):
        super().render(layer, cam)

        if self.state == 1:
            for content in self.get_content():
                content.render(layer, cam)

    def switched_event(self):
        if self.state == 0:
            for obj in self.get_content():
                if isinstance(obj, TerrainFolderLever):
                    obj.set_state(0)
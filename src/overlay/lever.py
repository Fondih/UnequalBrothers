from abc import ABC

import pygame as pg

from collider.collider import Collider
from overlay.button import Button


class Lever(Button, ABC):
    def __init__(self, pos, scaler=1):
        self.state = 0

        super().__init__(pos, scaler=scaler)

    @classmethod
    def create_name(cls):
        return "lever"

    @classmethod
    def create_state_max(cls):
        return 1

    @classmethod
    def is_anim(cls):
        return True

    @classmethod
    def get_anim_frames(cls):
        return cls.create_state_max() + 1

    def set_state(self, state):
        self.state = state
        self.switched_event()

    def switch_state(self):
        self.state += 1

        if self.state > self.create_state_max():
            self.state = 0

        self.switched_event()

    def get_texture_state(self, state):
        return self.get_texture()[state]

    def create_collider(self):
        return Collider(self.pos, Collider.Type.MOUSE, is_solid=False)

    def create_texture(self, colorkey_custom="black"):
        try:
            images = []
            for s in range(0, self.create_state_max() + 1):
                img = pg.image.load("assets/textures/overlay/" + self.create_namespace() +
                                    self.create_name() + "_" + str(s) + ".png").convert_alpha()
                img.set_colorkey(colorkey_custom)
                images.append(img)

            return images
        except FileNotFoundError:
            print("\033[31m" + "Cannot load images of lever:" + self.create_namespace() + self.create_name() + "\033[0m")

            images = []
            for s in range(0, self.create_state_max() + 1):
                img = pg.image.load("assets/textures/missing_texture.png").convert()
                images.append(img)

            return images

    def create_image(self):
        images = []

        for s in range(0, self.create_state_max() + 1):

            img = self.get_texture()[s]
            img = pg.transform.scale(img, self.create_texture_size())
            img = pg.transform.scale_by(img, self.scaler)
            img = pg.transform.rotate(img, self.rot)
            images.append(img)

        return images

    def render(self, layer, cam):
        layer.blit(self.image[self.state], self.pos.tuple())

    def clicked(self):
        self.switch_state()

        if self.create_state_max() <= 1:
            match self.state:
                case 0:
                    self.disabled()
                case 1:
                    self.enabled()

    def switched_event(self):
        pass

    def effect(self):
        pass

    def enabled(self):   # only work properly for levers w/ 2 states
        pass

    def disabled(self):   # only work properly for levers w/ 2 states
        pass

    def update(self):
        super().update()

        self.effect()
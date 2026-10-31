import pygame as pg

from run_modes import RunModes

#setup
WIDTH = 1280
HEIGHT = 720
CAPTION_DEFAULT = "Unequal Brothers"
FPS_MAX = 120
DT_MAX = 0.5

#game
FONT_DEFAULT = "Comic Sans MS"
ROOM_WIDTH = 2560
ROOM_HEIGHT = 1440
GRID_SIZE = 50
ROOM_START = "room_0"
GAMEMODE = RunModes.EDITOR

#editor
CAPTION_EDITOR = "Level Editor"
KEY_SUBTLE_EDITING = pg.KMOD_CTRL
KEY_EDITING_DRAG = 0
KEY_EDITING_PAINT = 2

#player input keys
K_UP = pg.K_w
K_DOWN = pg.K_s
K_LEFT = pg.K_a
K_RIGHT = pg.K_d
K_JUMP = pg.K_SPACE

#entity
PLAYER_SPEED = 400
PLAYER_JUMP_POWER = 7.4
PLAYER_SIZE_MOD = 1
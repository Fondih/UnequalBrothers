import pygame as pg

from run_modes import RunModes

#setup
WIDTH = 1280
HEIGHT = 720
CAPTION_DEFAULT = "Unequal Brothers"
FPS_MAX = 1200
DT_MAX = 0.5

#game
FONT_DEFAULT = "Comic Sans MS"
GRID_SIZE = 50
ROOM_START = "room_start_new"
GAMEMODE = RunModes.EDITOR

#editor
CAPTION_EDITOR = "Level Editor"
KEY_SUBTLE_EDITING = pg.KMOD_CTRL
KEY_DISCARD_SELECTED = pg.K_BACKSPACE
KEY_COMMIT_SELECTED = pg.K_RETURN
KEY_EDITING_DRAG = 0
KEY_EDITING_PAINT = 2
KEY_EDITING_PICK = 1

#player input keys
#player Big
K_UP_B = pg.K_w
K_DOWN_B = pg.K_s
K_LEFT_B = pg.K_a
K_RIGHT_B = pg.K_d

#player small
K_UP_S = pg.K_UP
K_DOWN_S = pg.K_DOWN
K_LEFT_S = pg.K_LEFT
K_RIGHT_S = pg.K_RIGHT

#entity
PLAYER_SPEED = 400
PLAYER_JUMP_POWER = 7.4
PLAYER_SIZE_MOD = 1
import pygame as pg
from termcolor import colored

import config as c
from _devtools.level_editor.overlay.editing_menu.terrain_place_lever import TerrainPlaceLever
from _devtools.level_editor.overlay.grid.grid_visual_menu_lever import GridVisualMenuLever
from _devtools.level_editor.overlay.other.editor_export_button import EditorExportButton
from _devtools.level_editor.overlay.other.noclip_lever import NoclipLever
from _devtools.level_editor.overlay.other.undo_commit_button import UndoCommitButton
from datatype.coordinate import Coordinate
from datatype.coordinate_screen import CoordinateScreen
from engine import Engine
from entity.concrete.player.player_entity import PlayerEntity
from level.camera import Camera
from level.dt import Dt
from level.level import Level
from overlay.overlays.fps_display import FPSDisplay
from overlay.text import Text
from run_modes import RunModes

# decide gamemode, use RunModes.DEFAULT for intended gameplay
run_mode = RunModes.EDITOR

engine = Engine(run_mode)
engine.init()
level = Level.get_instance()

#prepare terrain
layer_overlay = level.s_layer_overlay

player = PlayerEntity(Coordinate(c.ROOM_WIDTH // 2, c.HEIGHT // 2))

level.add_entity(player)
level.add_overlay(FPSDisplay())

if run_mode == RunModes.EDITOR:
    terrain_place_lever = TerrainPlaceLever(CoordinateScreen(c.WIDTH - 70, 20))
    level.add_overlay(terrain_place_lever)
    level.add_overlay(terrain_place_lever.menu)
    level.add_overlay(UndoCommitButton(CoordinateScreen(c.WIDTH - 110, 30)))
    level.add_overlay(GridVisualMenuLever(CoordinateScreen(c.WIDTH - 150, 30)))
    level.add_overlay(NoclipLever(CoordinateScreen(c.WIDTH - 190, 30)))
    level.add_overlay(EditorExportButton(CoordinateScreen(20, 20)))
if run_mode == RunModes.HACKS:
    level.add_overlay(NoclipLever(CoordinateScreen(c.WIDTH - 60, 30)))

Engine.import_room("room_0")
try:
    player.change_pos(level.get_player_spawner(0)[0].get_player_spawn_pos())
except IndexError:
    print(colored("Could not find player spawner", "red"))
    player.change_pos(Coordinate(c.ROOM_WIDTH // 2, c.ROOM_HEIGHT // 2))

while engine.running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            engine.running = False

    #quit input
    if pg.key.get_pressed()[pg.K_ESCAPE]:
        engine.running = False

    #deltatime
    Dt.get_instance().tick()

    #update
    engine.update_entity()
    engine.update_level_entity()
    engine.update_overlay()

    #update camera
    Camera.get_instance().set_pos(player.pos)

    #draw
    engine.draw()
    engine.render_overlay()

    pg.display.flip()

    engine.clock.tick(c.FPS_MAX)

#quitgame
pg.quit()
import pygame as pg

import config as c

from datatype.coordinate import Coordinate
from engine import Engine
from level.camera import Camera
from level.dt import Dt
from level.level import Level


engine = Engine(c.GAMEMODE)
engine.init()
level = Level.get_instance()

layer_overlay = level.s_layer_overlay

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

    # update camera
    player = Engine.get_instance().player
    if player is not None:
        Camera.get_instance().set_pos(player.pos)
    else:
        Camera.get_instance().set_pos(Coordinate(0, 0))

    #draw
    engine.draw()
    engine.render_overlay()

    pg.display.flip()

    engine.clock.tick(c.FPS_MAX)

#quitgame
pg.quit()
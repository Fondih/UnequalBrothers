import pygame as pg

import config as c

from datatype.coordinate import Coordinate
from engine import Engine, CamMode
from level.dt import Dt
from level.level import Level


engine = Engine()
engine.init()
level = Level.get_instance()

while engine.running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            engine.running = False

    #quit input
    if pg.key.get_pressed()[pg.K_ESCAPE]:
        engine.running = False

    #deltatime
    Dt.inst().tick()

    #update
    engine.update_controllers()
    engine.update_entity()
    engine.update_terrain()
    engine.update_overlay()

    # update camera
    try:
        player_big = Engine.inst().players["big"]
        player_small = Engine.inst().players["small"]
    except KeyError:
        player_big = None
        player_small = None
    if Engine.inst().cam_mode == CamMode.SPLIT and player_big is not None and player_small is not None:
        Engine.inst().cams["big"].set_pos(player_big.pos)
        Engine.inst().cams["small"].set_pos(player_small.pos)

    #draw
    if Engine.inst().cam_mode == CamMode.FULL:
        engine.draw("full")
    elif Engine.inst().cam_mode == CamMode.SPLIT:
        engine.draw("left")
        engine.draw("right")

    engine.render_overlay_sided()
    engine.render_sided()
    engine.render_overlay_full()

    pg.display.flip()

    engine.clock.tick(c.FPS_MAX)

#quitgame
pg.quit()
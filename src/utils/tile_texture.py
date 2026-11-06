import pygame as pg


def tile_texture(texture, t_width, t_height, width, height, has_alpha=False):
    """Scale `texture` by `scaler`, then tile it to fill a (width, height) surface."""
    tile = pg.transform.scale(texture, (t_width, t_height))
    if t_width == 0 or t_height == 0:
        raise ValueError("scaler shrinks the texture below 1px")

    colorkey = texture.get_colorkey()

    out = pg.Surface((width, height), pg.SRCALPHA if has_alpha else 0)
    if colorkey is not None:
        out.fill(colorkey)  # so keyed pixels in the tiles stay keyed

    out.blits([(tile, (x, y))
               for y in range(0, height, t_width)
               for x in range(0, width, t_height)], doreturn=False)

    if colorkey is not None:
        out.set_colorkey(colorkey)

    # match the display format so later blits stay on the fast path
    return out
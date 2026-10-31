import pygame as pg

def nine_slice(src, size, border):
    """Scale src to `size`, keeping the corners undistorted.
    border = (left, top, right, bottom) in source pixels."""
    l, t, r, b = border
    sw, sh = src.get_size()
    w = max(size[0], l + r)   # can't be smaller than the corners
    h = max(size[1], t + b)

    xs_src = [0, l, sw - r, sw]
    ys_src = [0, t, sh - b, sh]
    xs_dst = [0, l, w - r, w]
    ys_dst = [0, t, h - b, h]

    out = pg.Surface((w, h), pg.SRCALPHA)
    for i in range(3):
        for j in range(3):
            src_rect = pg.Rect(xs_src[i], ys_src[j],
                               xs_src[i + 1] - xs_src[i], ys_src[j + 1] - ys_src[j])
            dst_rect = pg.Rect(xs_dst[i], ys_dst[j],
                               xs_dst[i + 1] - xs_dst[i], ys_dst[j + 1] - ys_dst[j])
            if src_rect.w <= 0 or src_rect.h <= 0 or dst_rect.w <= 0 or dst_rect.h <= 0:
                continue
            piece = src.subsurface(src_rect)
            if piece.get_size() != dst_rect.size:
                piece = pg.transform.scale(piece, dst_rect.size)
            out.blit(piece, dst_rect)
    return out
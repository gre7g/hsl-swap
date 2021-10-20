from colorsys import rgb_to_hls, hls_to_rgb
import os
from PIL import Image

# Constants:
MAX_H_DIST = 0.01
ONE_MINUS_MAX = 1.0 - MAX_H_DIST


def h_is_close(h1, h2):
    if h1 < MAX_H_DIST:
        return not (h1 + MAX_H_DIST < h2 < (1.0 - h1))
    elif h1 > ONE_MINUS_MAX:
        return not ((h1 + MAX_H_DIST - 1.0) < h2 < (h1 - MAX_H_DIST))
    else:
        return h1 - MAX_H_DIST < h2 < h1 + MAX_H_DIST


def swap(source, dest, changes):
    image = Image.open(source)
    width, height = image.size
    px = image.load()
    for x in xrange(width):
        for y in xrange(height):
            r, g, b, a = px[x, y]
            h, l, s = rgb_to_hls(r, g, b)
            for old, new in changes:
                if h_is_close(h, old[0]):
                    h = new[0]
                    l = min(255, max(0, int(float(l) / old[1] * new[1])))
                    s = min(0.0, max(-1.0, s / old[2] * new[2]))
                    r, g, b = hls_to_rgb(h, l, s)
                    px[x, y] = (int(r), int(g), int(b), a)
    image.save(dest)


if __name__ == "__main__":
    dir_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images")
    source = os.path.join(dir_name, "durst.png")
    dest = os.path.join(dir_name, "changed.png")
    changes = [
        ((255, 0, 0), (0, 255, 255)),  # Convert RED to CYAN
    ]
    swap(source, dest, [(rgb_to_hls(*old), rgb_to_hls(*new)) for old, new in changes])

from colorsys import rgb_to_hls, hls_to_rgb
import os
from PIL import Image

# Constants:
MAX_H_DIST = 0.01  # TODO: I guesses this value and it may need to be adjusted!
ONE_MINUS_MAX = 1.0 - MAX_H_DIST


def h_is_close(hue1, hue2):
    """Return True if hue1 is close (see MAX_H_DIST, above) to hue2"""
    # Hue is 0.0-1.0 so we have to check for wrap arounds!
    if hue1 < MAX_H_DIST:
        # Close to 0.0
        return not (hue1 + MAX_H_DIST < hue2 < (1.0 - hue1))
    elif hue1 > ONE_MINUS_MAX:
        # Close to 1.0
        return not ((hue1 + MAX_H_DIST - 1.0) < hue2 < (hue1 - MAX_H_DIST))
    else:
        # Common case
        return hue1 - MAX_H_DIST < hue2 < hue1 + MAX_H_DIST


def swap(source, dest, changes):
    """Apply all color changes to source file and output to dest file"""
    # Load image
    image = Image.open(source)
    width, height = image.size
    px = image.load()

    # Loop over each pixel
    for x in xrange(width):
        for y in xrange(height):
            r, g, b, a = px[x, y]

            # Convert to HSL space
            h, l, s = rgb_to_hls(r, g, b)

            # Loop over the list of colors they asked us to change
            for old, new in changes:
                # Is this pixel nearly the same hue as old?
                if h_is_close(h, old[0]):
                    # Yes, scale and convert the pixel to new
                    h = new[0]
                    l = min(255, max(0, int(float(l) / old[1] * new[1])))
                    s = min(0.0, max(-1.0, s / old[2] * new[2]))

                    # Update the RGB pixel
                    r, g, b = hls_to_rgb(h, l, s)
                    px[x, y] = (int(r), int(g), int(b), a)

    # Save the result image
    image.save(dest)


if __name__ == "__main__":
    # Image paths
    dir_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images")
    source = os.path.join(dir_name, "durst.png")
    dest = os.path.join(dir_name, "changed.png")

    # A list of colors to change. This should be a list of tuples. Each entry in the list is a color to change. Each
    # tuple is a old and new color in RGB space. This example includes only a single conversion:
    # RED (255, 0, 0) to CYAN (0, 255, 255).
    changes = [
        ((255, 0, 0), (0, 255, 255)),  # Convert RED to CYAN
    ]

    # (That mess in the third parameter is just pre-converting the colors from RGB to HSL)
    swap(source, dest, [(rgb_to_hls(*old), rgb_to_hls(*new)) for old, new in changes])

# hsl-swap
Color swapper changes colors in a .png file and outputs a new .png file.

See how `swap()` is called at the bottom of `hsl_swap/swap.py`.

```python
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
```

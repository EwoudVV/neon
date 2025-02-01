# Made by Ewoud Van Vooren on 1/31/25 for Hack Club Neon

import random
import time

import board
import displayio
import framebufferio
import rgbmatrix

displayio.release_displays()

def apply_meteor_shower(bitmap, palette, trail_length=8):
    width = bitmap.width
    height = bitmap.height
    for i in range(width * height):
        bitmap[i] = 0

    meteors = [
        {
            "x": random.randint(0, width - 1),
            "y": random.randint(0, height - 1),
            "trail": [None] * trail_length,
            "direction": (random.choice([-1, 0, 1]), random.choice([-1, 1])),
            "lifespan": 10,
        }
        for _ in range(5)
    ]

    for _ in range(100):
        for meteor in meteors:
            meteor["trail"].insert(0, (meteor["x"], meteor["y"]))
            if len(meteor["trail"]) > trail_length:
                trail_pos = meteor["trail"].pop()
                if trail_pos is not None:
                    trail_x, trail_y = trail_pos
                    if 0 <= trail_x < width and 0 <= trail_y < height:
                        bitmap[trail_x + trail_y * width] = 0

            meteor["x"] += meteor["direction"][0]
            meteor["y"] += meteor["direction"][1]
            meteor["lifespan"] -= 1

            if meteor["lifespan"] <= 0 or meteor["x"] < 0 or meteor["x"] >= width or meteor["y"] < 0 or meteor["y"] >= height:
                meteor["x"] = random.randint(0, width - 1)
                meteor["y"] = random.randint(0, height - 1)
                meteor["trail"] = [None] * trail_length
                meteor["direction"] = (random.choice([-1, 0, 1]), random.choice([-1, 1]))
                meteor["lifespan"] = 10

            for trail_pos in meteor["trail"]:
                if trail_pos is not None:
                    trail_x, trail_y = trail_pos
                    if 0 <= trail_x < width and 0 <= trail_y < height:
                        bitmap[trail_x + trail_y * width] = 1

        display.root_group = g1 if display.root_group == g2 else g2
        display.refresh()
        time.sleep(0.05)

matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1
)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)
SCALE = 1
bitmap = displayio.Bitmap(display.width // SCALE, display.height // SCALE, 2)
palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0xC0C0C0
tg = displayio.TileGrid(bitmap, pixel_shader=palette)
group = displayio.Group(scale=SCALE)
group.append(tg)
display.root_group = group

g1 = displayio.Group(scale=SCALE)
g1.append(displayio.TileGrid(bitmap, pixel_shader=palette))
g2 = displayio.Group(scale=SCALE)
g2.append(displayio.TileGrid(bitmap, pixel_shader=palette))

apply_meteor_shower(bitmap, palette)

import time
import board
import digitalio
import usb_hid
import neopixel
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# ------------------
# Setup
# ------------------
kbd = Keyboard(usb_hid.devices)
pixels = neopixel.NeoPixel(board.D2, 2, brightness=0.4, auto_write=True)

button_map = [
    (board.D26, Keycode.W),
    (board.D27, Keycode.A),
    (board.D28, Keycode.S),
    (board.D29, Keycode.D),
]

buttons = []
for pin, key in button_map:
    btn = digitalio.DigitalInOut(pin)
    btn.switch_to_input(pull=digitalio.Pull.UP)
    buttons.append({"obj": btn, "key": key, "pressed": False})

# ------------------
# Rainbow Function
# ------------------
def rainbow_cycle(step):
    # step = 0–255
    r = (step & 255)
    g = (step * 2 & 255)
    b = (step * 3 & 255)
    pixels.fill((r, g, b))  # BOTH LEDs same color

rainbow_step = 0
rainbow_active = True

# ------------------
# Main Loop
# ------------------
while True:
    any_pressed = False

    for b in buttons:
        if not b["obj"].value:   # pressed
            any_pressed = True
            if not b["pressed"]:
                kbd.press(b["key"])
                b["pressed"] = True

            # Same color for both LEDs
            if b["key"] == Keycode.W:
                pixels.fill((0, 0, 255))
            elif b["key"] == Keycode.A:
                pixels.fill((255, 0, 0))
            elif b["key"] == Keycode.S:
                pixels.fill((0, 255, 0))
            elif b["key"] == Keycode.D:
                pixels.fill((255, 255, 0))

        else:  # released
            if b["pressed"]:
                kbd.release(b["key"])
            b["pressed"] = False

    # If no keys pressed → resume rainbow
    if not any_pressed:
        rainbow_active = True
        rainbow_cycle(rainbow_step)
        rainbow_step = (rainbow_step + 1) % 256
        time.sleep(0.02)
    else:
        rainbow_active = False
        time.sleep(0.01)

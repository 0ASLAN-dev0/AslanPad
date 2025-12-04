import time
import board
import digitalio
import usb_hid
import neopixel
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# ======================
# HID Setup
# ======================
kbd = Keyboard(usb_hid.devices)

# ======================
# Buttons
# ======================
button_map = [
    (board.D26, Keycode.D),  # Key 1
    (board.D27, Keycode.W),  # Key 2
    (board.D28, Keycode.A),  # Key 3
    (board.D29, Keycode.S),  # Key 4
]

buttons = []
for pin, keycode in button_map:
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    buttons.append({"pin": btn, "key": keycode, "state": False})

# ======================
# RGB LEDs
# ======================
LED_PIN = board.D2
NUM_LEDS = 2
pixels = neopixel.NeoPixel(LED_PIN, NUM_LEDS, brightness=0.4, auto_write=True)

# Key colors
COLOR_W = (0, 0, 255)
COLOR_A = (0, 255, 0)
COLOR_S = (255, 0, 255)
COLOR_D = (255, 0, 0)

# Track keypress to pause rainbow
key_active = False


# ======================
# Rainbow Animation
# ======================
def wheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def rainbow_step(offset):
    for i in range(NUM_LEDS):
        pixel_index = (i * 256 // NUM_LEDS) + offset
        pixels[i] = wheel(pixel_index & 255)


offset = 0


# ======================
# Main Loop
# ======================
while True:
    any_pressed = False

    for i, info in enumerate(buttons):
        pin = info["pin"]
        keycode = info["key"]

        if not pin.value:  # pressed (LOW)
            any_pressed = True

            if not info["state"]:
                kbd.press(keycode)
                info["state"] = True

                # Set press color
                if keycode == Keycode.W:
                    pixels.fill(COLOR_W)
                elif keycode == Keycode.A:
                    pixels.fill(COLOR_A)
                elif keycode == Keycode.S:
                    pixels.fill(COLOR_S)
                elif keycode == Keycode.D:
                    pixels.fill(COLOR_D)
        else:
            # key released
            if info["state"]:
                kbd.release(keycode)
                info["state"] = False

    # Rainbow resumes ONLY if no key is held
    if not any_pressed:
        offset = (offset + 3) % 256
        rainbow_step(offset)

    time.sleep(0.01)

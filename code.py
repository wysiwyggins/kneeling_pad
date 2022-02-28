
import time
import board
import neopixel
import digitalio
import usb_hid

from adafruit_hid.keyboard import Keyboard 
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_debouncer import Debouncer

button_fire = digitalio.DigitalInOut(board.D5)
button_fire.direction = digitalio.Direction.INPUT
button_fire.pull = digitalio.Pull.UP

button_up = digitalio.DigitalInOut(board.D6)
button_up.direction = digitalio.Direction.INPUT
button_up.pull = digitalio.Pull.UP

button_down = digitalio.DigitalInOut(board.D9)
button_down.direction = digitalio.Direction.INPUT
button_down.pull = digitalio.Pull.UP

button_left = digitalio.DigitalInOut(board.D10)
button_left.direction = digitalio.Direction.INPUT
button_left.pull = digitalio.Pull.UP

button_right = digitalio.DigitalInOut(board.D11)
button_right.direction = digitalio.Direction.INPUT
button_right.pull = digitalio.Pull.UP

button_kneel = digitalio.DigitalInOut(board.D12)
button_kneel.direction = digitalio.Direction.INPUT
button_kneel.pull = digitalio.Pull.UP

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

time.sleep(1)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

while True: 
    if not button_fire.value:
        led.value = True
        keyboard_layout.write(Keycode.ENTER)
    elif not button_up.value:
        led.value = True
        keyboard_layout.write(Keycode.UP_ARROW)
    elif not button_down.value:
        led.value = True
        keyboard_layout.write(Keycode.DOWN_ARROW)
    elif not button_left.value:
        led.value = True
        keyboard_layout.write(Keycode.LEFT_ARROW)
    elif not button_right.value:
        led.value = True
        keyboard_layout.write(Keycode.RIGHT_ARROW)
    elif not button_kneel.value:
        led.value = True
        keyboard_layout.write("p")
    else:
        led.value = False
        keyboard.release_all()
    time.sleep(0.01)





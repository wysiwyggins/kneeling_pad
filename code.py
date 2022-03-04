import time
import board
import digitalio
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from adafruit_debouncer import Debouncer

def createButton(pinRef):
  btn = digitalio.DigitalInOut(pinRef)
  btn.direction = digitalio.Direction.INPUT
  btn.pull = digitalio.Pull.UP
  return btn

button_fire = createButton(board.D5)
button_up = createButton(board.D10)
button_down = createButton(board.D11)
button_left = createButton(board.D6)
button_right = createButton(board.D9)

pin_kneel = digitalio.DigitalInOut(board.D12)
pin_kneel.direction = digitalio.Direction.INPUT
pin_kneel.pull = digitalio.Pull.UP
button_kneel = Debouncer(pin_kneel)




led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

time.sleep(1)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)


    
while True:
    button_kneel.update()
    if not button_fire.value:
        led.value = True
        keyboard.press(Keycode.ENTER)
    elif not button_up.value:
        led.value = True
        keyboard.press(Keycode.UP_ARROW)
    elif not button_down.value:
        led.value = True
        keyboard.press(Keycode.DOWN_ARROW)
    elif not button_left.value:
        led.value = True
        keyboard.press(Keycode.LEFT_ARROW)
    elif not button_right.value:
        led.value = True
        keyboard.press(Keycode.RIGHT_ARROW)
    elif button_kneel.fell:
        led.value = True
        keyboard_layout.write("p")
    else:
        led.value = False
        keyboard.release_all()
    time.sleep(0.01)
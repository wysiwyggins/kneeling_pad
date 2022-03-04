import time
import board
import digitalio
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from adafruit_debouncer import Debouncer

#from adafruit_ble import BLERadio
#from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
#from adafruit_ble.services.nordic import UARTService

#from adafruit_airlift.esp32 import ESP32

def createButton(pinRef):
  btn = digitalio.DigitalInOut(pinRef)
  btn.direction = digitalio.Direction.INPUT
  btn.pull = digitalio.Pull.UP
  return btn

button_fire = createButton(board.A0)
button_up = createButton(board.A3)
button_down = createButton(board.D5)
button_left = createButton(board.A1)
button_right = createButton(board.A2)
pin_kneel = digitalio.DigitalInOut(board.D6)
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
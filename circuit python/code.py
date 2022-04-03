import time
import board
import digitalio
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

from adafruit_debouncer import Debouncer

# from adafruit_ble import BLERadio
# from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
# from adafruit_ble.services.nordic import UARTService

# from adafruit_airlift.esp32 import ESP32

# esp32 = ESP32(
#     reset=board.D12,
#     gpio0=board.D10,
#     busy=board.D11,
#     chip_select=board.D13,
#     tx=board.TX,
#     rx=board.RX,
# )

# adapter = esp32.start_bluetooth()

# ble = BLERadio(adapter)
# uart = UARTService()
# advertisement = ProvideServicesAdvertisement(uart)

# while True:
#     ble.start_advertising(advertisement)
#     print("waiting to connect")
#     while not ble.connected:
#         pass
#     print("connected: trying to read input")
#     while ble.connected:
#         # Returns b'' if nothing was read.
#         one_byte = uart.read(1)
#         if one_byte:
#             print(one_byte)
#             uart.write(one_byte)

def createButton(pinRef):
  btn = digitalio.DigitalInOut(pinRef)
  btn.direction = digitalio.Direction.INPUT
  btn.pull = digitalio.Pull.UP
  return btn

#button_fire = createButton(board.A0)
button_up = createButton(board.A3)
button_down = createButton(board.D24)
button_left = createButton(board.A1)
button_right = createButton(board.A2)

pin_fire = digitalio.DigitalInOut(board.A0)
pin_fire.direction = digitalio.Direction.INPUT
pin_fire.pull = digitalio.Pull.UP
button_fire = Debouncer(pin_fire)

pin_kneel = digitalio.DigitalInOut(board.D25)
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
    button_fire.update()

    if button_fire.fell:
        led.value = True
        keyboard.press(Keycode.ENTER)
    elif button_fire.rose:
        led.value = False
        keyboard.release(Keycode.ENTER)

    if not button_up.value:
        led.value = True
        keyboard.press(Keycode.UP_ARROW)
    else:
        keyboard.release(Keycode.UP_ARROW)
    
    if not button_down.value:
        led.value = True
        keyboard.press(Keycode.DOWN_ARROW)
    else:
        keyboard.release(Keycode.DOWN_ARROW)

    if not button_left.value:
        led.value = True
        keyboard.press(Keycode.LEFT_ARROW)
    else:
        keyboard.release(Keycode.LEFT_ARROW)

    if not button_right.value:
        led.value = True
        keyboard.press(Keycode.RIGHT_ARROW)
    else:
        led.value = False
        keyboard.release(Keycode.RIGHT_ARROW)

    if button_kneel.fell:
        led.value = True
        keyboard_layout.press("p")
    elif button_kneel.rose:
        led.value = False
        keyboard_layout.release("p")

    time.sleep(0.01)
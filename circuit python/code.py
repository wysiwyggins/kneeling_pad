"""
Connects to mqtt server
"""
import board
import busio
import neopixel
from digitalio import DigitalInOut, Pull, Direction
from adafruit_debouncer import Debouncer
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager

from mqtt import connectToMQTT
from secrets import secrets

# this is just a demo of listening
def onToggleTopic():
  print("TOGGLE")

def connectToWifi(secrets, esp):
  print("\n\nconnectToWifi")
  print("Connecting to %s..." % secrets["ssid"])
  status_light = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)
  wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(
    esp,
    secrets,
    status_light
  )
  wifi.connect()
  print("Connected to %s!" % secrets["ssid"])
  return wifi

# Connect to wifi via spi
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

connectToWifi(secrets, esp)

# create mqtt
mqtt_client = connectToMQTT(secrets, esp, {
  "test/toggle": onToggleTopic
})

# setup the button
pin = DigitalInOut(board.D9)
pin.direction = Direction.INPUT
pin.pull = Pull.UP
switch = Debouncer(pin)

while True:
  mqtt_client.loop()
  switch.update()
  if switch.rose:
    print("Sending topic `action/unkneel`")
    mqtt_client.publish("action/unkneel", 1)
  elif switch.fell:
    print("Sending topic `action/kneel`")
    mqtt_client.publish("action/kneel", 1)

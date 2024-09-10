import board
import busio
import neopixel
from digitalio import DigitalInOut, Pull, Direction
from adafruit_debouncer import Debouncer
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager

from mqtt import connectToMQTT
from secrets import secrets

# This is just a demo of listening
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

# Connect to Wi-Fi via SPI
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

wifi = connectToWifi(secrets, esp)

# Create MQTT
try:
    mqtt_client = connectToMQTT(secrets, esp, {
        "test/toggle": onToggleTopic
    })
except Exception as e:
    print("Failed to connect to MQTT: ", e)
    mqtt_client = None

# Setup the button
pin = DigitalInOut(board.D9)
pin.direction = Direction.INPUT
pin.pull = Pull.UP
switch = Debouncer(pin)

counter = DigitalInOut(board.D8)
counter.direction = Direction.OUTPUT

while True:
    try:
        # Increment mechanical counter regardless of MQTT status
        switch.update()
        if switch.rose:
            print("Button pressed: incrementing counter")
            counter.value = False
            if mqtt_client:  # Only publish if MQTT client is available
                print("Sending topic `kneels/set`")
                mqtt_client.publish("kneels/set", 1)
        elif switch.fell:
            print("Button released: incrementing counter")
            counter.value = True
            if mqtt_client:  # Only publish if MQTT client is available
                print("Sending topic `kneels/set`")
                mqtt_client.publish("kneels/set", 0)

        # Run MQTT loop only if the client is available
        if mqtt_client:
            mqtt_client.loop()

    except Exception as e:
        print("An error occurred: ", e)
        print("Attempting to reconnect to WiFi and MQTT...")
        try:
            wifi.reset()
            wifi.connect()
            if mqtt_client:
                mqtt_client.reconnect()
        except Exception as e:
            print("Failed to reconnect, error: ", e)
        continue

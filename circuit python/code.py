import board
import digitalio
import busio
import digitalio
import neopixel
import adafruit_debouncer
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import time
from digitalio import DigitalInOut
import adafruit_requests as requests
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise


# Define digital input for button
button_pin = digitalio.DigitalInOut(board.D7)
button_pin.direction = digitalio.Direction.INPUT
button_pin.pull = digitalio.Pull.UP
button = adafruit_debouncer.Debouncer(button_pin)

# Define neopixel to indicate button presses
pixels = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)

# If you are using a board with pre-defined ESP32 Pins:
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)


spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
mqtt = MQTT.MQTT(broker=secrets["broker"], port=secrets["port"])


def message_received(topic, msg):
    print("Received message from topic '{}': {}".format(topic, msg))


# Define function to handle button presses
def handle_button_press(pin):
    if not button.value:
        # Turn on neopixel
        pixels.fill((255, 0, 0))
        # Publish MQTT message
        mqtt.publish("kneels/get", "Knelt in devotion")
        # Wait a bit to debounce
        time.sleep(0.1)
        # Turn off neopixel
        pixels.fill((0, 0, 0))


# Attach button interrupt
button.when_pressed = handle_button_press

if esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
    print("ESP32 found and in idle mode")
print("Firmware vers.", esp.firmware_version)
print("MAC addr:", [hex(i) for i in esp.MAC_address])

for ap in esp.scan_networks():
    print("\t%s\t\tRSSI: %d" % (str(ap["ssid"], "utf-8"), ap["rssi"]))

print("Connecting to AP...")
while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except OSError as e:
        print("could not connect to AP, retrying: ", e)
        continue
print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)
print("My IP address is", esp.pretty_ip(esp.ip_address))

# Connect to MQTT broker
print("Connecting to MQTT broker...")
mqtt.connect()
print("Connected to MQTT broker")

# Loop forever, handling MQTT messages and button presses
while True

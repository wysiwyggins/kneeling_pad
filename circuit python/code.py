# SPDX-FileCopyrightText: 2019 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import digitalio
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_minimqtt.adafruit_minimqtt as MQTT

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise


# If you are using a board with pre-defined ESP32 Pins:
esp32_cs = digitalio.DigitalInOut(board.D10)
esp32_ready = digitalio.DigitalInOut(board.D9)
esp32_reset = digitalio.DigitalInOut(board.D5)


spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

mqtt = MQTT.MQTT(esp, secrets["broker"], "1883")

def message_received(topic, msg):
    print("Received message from topic '{}': {}".format(topic, msg))


# Subscribe to the API at mudroom.rip using the security token
security_token = secrets["token"]
mqtt.subscribe("JSON_URL" + security_token, message_received)

# Define a button and a flag to keep track of its state
button = digitalio.DigitalInOut(board.D7)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

button_state = False

# Define the callback function for the button
def button_callback(change):
    global button_state
    button_state = not button_state
    mqtt.publish("mudroom.rip/api/v1/game/rooms/kneel/", str(button_state), qos=0)

# Attach the button callback function to the button
button.callback = button_callback

while True:
    mqtt.loop()
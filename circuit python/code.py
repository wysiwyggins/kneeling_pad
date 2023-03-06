
import board
import busio
import digitalio
import time
from adafruit_esp32spi import adafruit_esp32spi_socket as socket
import adafruit_minimqtt.adafruit_minimqtt as MQTT

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Set up ESP32 SPI connection
esp32_cs = digitalio.DigitalInOut(board.D9)
esp32_ready = digitalio.DigitalInOut(board.D10)
esp32_reset = digitalio.DigitalInOut(board.D5)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

# Connect to WiFi
print("Connecting to WiFi...")
while not esp.is_connected:
    try:
        esp.connect_AP("ssid", "password")
    except RuntimeError as e:
        print("Could not connect to WiFi, retrying...")
        continue
print("Connected to WiFi")

# Set up MQTT client
mqtt_broker = "192.168.50.93"
mqtt_topic = "kneels/get"
client_id = "circuitpython_client"
mqtt_client = MQTT.MQTT(socket, broker=mqtt_broker, client_id=client_id)

# Define button pin
button = digitalio.DigitalInOut(board.D7)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Define function to publish message on button press
def on_button_press(_):
    message = "Knelt in devotion at {}".format(time.monotonic())
    print("Publishing message: ", message)
    mqtt_client.publish(mqtt_topic, message)

# Set up button interrupt
button.add_event_detect(digitalio.EdgeFalling, callback=on_button_press)

# Connect to MQTT broker
print("Connecting to MQTT broker...")
while not mqtt_client.is_connected:
    try:
        esp.start_ssl(mqtt_broker)
        socket.set_interface(esp)
        mqtt_client.connect()
    except socket.gaierror as e:
        print("Could not connect to MQTT broker, retrying...")
        time.sleep(1)
print("Connected to MQTT broker")

while True:
    mqtt_client.loop()
    time.sleep(1)

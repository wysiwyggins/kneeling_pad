import adafruit_minimqtt.adafruit_minimqtt as MQTT
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
#import ssl

topicMap = {}

# This function will be called when the mqttClient is connected successfully to the broker.
def onConnect(mqttClient, userdata, flags, rc):
    print("Connected to MQTT Broker!")
    print("Flags: {0}\nRC: {1}".format(flags, rc))

# This method is called when the mqttClient disconnects from the broker.
def onDisconnect(mqttClient, userdata, rc):
    print("Disconnected from MQTT Broker")

# This method is called when the mqttClient subscribes to a new feed.
def onSubscribe(mqttClient, userdata, topic, granted_qos):
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))

# This method is called when the mqttClient publishes data to a feed.
def onPublish(mqttClient, userdata, topic, pid):
    print("Published to {0} with PID {1}".format(topic, pid))

# Method callled when a client's subscribed feed has a new value.
def onMessage(client, topic, message):
    print("New message on topic {0}: {1}".format(topic, message))
    try:
      method = topicMap[topic]
      method()
    except Exception:
      print("Nothing named %s found in" % topic)
      print(topicMap)
      pass

def connectToMQTT(secrets, esp, topics):
  MQTT.set_socket(socket, esp)
  mqttClient = MQTT.MQTT(
    broker=secrets["broker"],
    port=secrets["port"],
    ssl_context=ssl.create_default_context(),
  )
  
  # Connect callback handlers to mqttClient
  mqttClient.on_connect = onConnect
  mqttClient.on_disconnect = onDisconnect
  mqttClient.on_subscribe = onSubscribe
  mqttClient.on_publish = onPublish
  mqttClient.on_message = onMessage

  print("Attempting to connect broker at: %s" % mqttClient.broker)
  mqttClient.connect()

  # copy topics to local var
  global topicMap
  topicMap = topics.copy()

  for topic in topics.keys():
    print("Subscribing to %s" % topic)
    mqttClient.subscribe(topic)

  return mqttClient

import paho.mqtt.client as mqtt

# ---------------------------------------
# MQTT Configuration
# ---------------------------------------

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "sensors/temperature_humidity"


# ---------------------------------------
# Callback function when connected
# ---------------------------------------

def on_connect(client, userdata, flags, reason_code, properties):

    if reason_code == 0:

        print("Connected successfully to HiveMQ broker!")
        print("Subscribing to topic:", TOPIC)
        print("---------------------------------------")

        # Subscribe to topic
        client.subscribe(TOPIC)

    else:

        print("Connection failed.")
        print("Reason code:", reason_code)


# ---------------------------------------
# Callback function when message arrives
# ---------------------------------------

def on_message(client, userdata, message):

    received_message = message.payload.decode("utf-8")

    print("Message received:")
    print("Topic   :", message.topic)
    print("Message :", received_message)
    print("---------------------------------------")


# ---------------------------------------
# Create MQTT Client
# ---------------------------------------

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    "temperature_humidity_subscriber"
)

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message


# ---------------------------------------
# Connect to HiveMQ
# ---------------------------------------

print("Connecting to HiveMQ broker...")

client.connect(BROKER, PORT)

# ---------------------------------------
# Start MQTT network loop
# ---------------------------------------

try:

    client.loop_forever()

except KeyboardInterrupt:

    print("\nSubscriber stopped.")

finally:

    client.disconnect()
    print("Disconnected from broker.")

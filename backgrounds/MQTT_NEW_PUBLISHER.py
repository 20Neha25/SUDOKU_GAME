import paho.mqtt.client as mqtt
import time
import random

# ---------------------------------------
# MQTT Configuration
# ---------------------------------------

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "sensors/temperature_humidity"

# ---------------------------------------
# Create MQTT Client
# ---------------------------------------

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    "temperature_humidity_publisher"
)

# ---------------------------------------
# Connect to HiveMQ Broker
# ---------------------------------------

print("Connecting to HiveMQ broker...")

client.connect(BROKER, PORT)

print("Connected successfully!")
print("Publishing sensor data...")
print("---------------------------------------")

# ---------------------------------------
# Publish sensor data
# ---------------------------------------

try:

    while True:

        # Generate simulated sensor values
        temperature = round(random.uniform(20.0, 30.0), 2)
        humidity = round(random.uniform(40.0, 60.0), 2)

        # Create message
        message = (
            f"Temperature: {temperature} °C, "
            f"Humidity: {humidity} %"
        )

        # Publish message
        result = client.publish(TOPIC, message)

        # Check whether publishing was successful
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print("Published:", message)
        else:
            print("Failed to publish message")

        # Wait 5 seconds
        time.sleep(5)

except KeyboardInterrupt:

    print("\nPublisher stopped.")

finally:

    client.disconnect()
    print("Disconnected from broker.")

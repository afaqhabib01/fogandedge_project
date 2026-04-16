# edge.py
import time
import random
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# Configure AWS IoT device
client = AWSIoTMQTTClient("edgedevice01")
client.configureEndpoint("a3eoyzapthcjew-ats.iot.us-east-1.amazonaws.com", 8883)
client.configureCredentials(
    "app/certificates/AmazonRootCA1.pem", 
    "app/certificates/private.pem.key", 
    "app/certificates/certificate.pem.crt"
)
client.connect()

INTERVAL = 15  # send data every 5 seconds

# Initial sensor values
water_level = 0
flow_rate = 0
temperature = 0
pressure = 0

def update_value(value, min_val, max_val, change_range):
    value += random.randint(-change_range, change_range)
    return max(min_val, min(max_val, value))

while True:
    # Simulate sensor readings
    water_level = update_value(water_level, 0, 100, 2)
    flow_rate = update_value(flow_rate, 0, 20, 1)
    temperature = update_value(temperature, 15, 40, 1)
    pressure = update_value(pressure, 900, 1100, 3)

    payload = {
        "water_level": water_level,
        "flow_rate": flow_rate,
        "temperature": temperature,
        "pressure": pressure,
        "timestamp": time.time()
    }

    # Publish to AWS IoT topic
    client.publish("water/sensor", json.dumps(payload), 1)
    print("📡 Published:", payload)

    time.sleep(INTERVAL)
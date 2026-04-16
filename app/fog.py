import json
import pymysql, time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


# -------------------------------
# DATABASE CONNECTION
# -------------------------------
db = pymysql.connect(
    host="database.cwt4o2i8a5c3.us-east-1.rds.amazonaws.com",
    user="admin",
    password="12345678",   # 🔴 CHANGE THIS
    database="edgedata"
)

cursor = db.cursor()

# -------------------------------
# MQTT CALLBACK FUNCTION
# -------------------------------
def message_callback(client, userdata, message):
    try:
        data = json.loads(message.payload)
        print("📥 Received:", data)

        water_level = data["water_level"]
        flow_rate = data["flow_rate"]
        temperature = data["temperature"]
        pressure = data["pressure"]

        min_water = 0
        max_water = 100

        alert = []

        if water_level > 90:
            alert.append("⚠️ High Water Level")
        elif water_level < 20:
            alert.append("⚠️ Low Water Level")

        if flow_rate > 95:
            alert.append("⚠️ High Water Flow")

        if temperature > 35:
            alert.append("⚠️ High Temperature")
        elif temperature < 7:
            alert.append("⚠️ Low Temperature")

        if pressure > 1000:
            alert.append("⚠️ High Pressure")

        alert_text = json.dumps(alert)

        # ✅ CREATE NEW DB CONNECTION HERE
        db = pymysql.connect(
            host="database.cwt4o2i8a5c3.us-east-1.rds.amazonaws.com",
            user="admin",
            password="12345678",
            database="edgedata"
        )

        cursor = db.cursor()

        sql = """
        INSERT INTO sensor_data 
        (water_level, flow_rate, temperature, pressure, min_water, max_water, alerts, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            water_level,
            flow_rate,
            temperature,
            pressure,
            min_water,
            max_water,
            alert_text,
            data["timestamp"]
        )

        cursor.execute(sql, values)
        db.commit()

        print("✅ Data saved to RDS database")

        db.close()   # ✅ CLOSE CONNECTION

    except Exception as e:
        print("❌ ERROR:", e)

# -------------------------------
# AWS IoT MQTT SETUP
# -------------------------------
client = AWSIoTMQTTClient("fogDevice01")

client.configureEndpoint(
    "a3eoyzapthcjew-ats.iot.us-east-1.amazonaws.com",
    8883
)

client.configureCredentials(
    "app/certificates/AmazonRootCA1.pem",
    "app/certificates/private.pem.key",
    "app/certificates/certificate.pem.crt"
)

client.connect()
print("✅ Connected to AWS IoT")

client.subscribe("water/sensor", 1, message_callback)

print("📡 Listening for sensor data...")

while True:
    time.sleep(1)
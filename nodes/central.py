import serial
import threading
import json
import time

SERIAL_PORT = "COM5"
BAUD = 115200
OUTPUT_FILE = "data.json"

ser = serial.Serial(SERIAL_PORT, BAUD, timeout=0.1)

SOLDIER_ID = "soldier_01"

def update_json(message="", lat=0.0, lon=0.0):
    data = {
        "id": SOLDIER_ID,
        "message": message,
        "location": {
            "latitude": lat,
            "longitude": lon
        },
        "timestamp": int(time.time())
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print("JSON file updated.")


def receive():
    while True:
        line = ser.readline().decode(errors='ignore').strip()

        if not line:
            continue

        print("<<", line)

        if "RX:[DATA]" in line:
            try:
                payload = line.split("RX:[DATA]")[-1].strip()
                message_part, gps_part = payload.split("|")

                message = message_part.strip()
                lat_str, lon_str = gps_part.strip().split(",")

                lat = float(lat_str)
                lon = float(lon_str)

                update_json(message, lat, lon)

            except Exception as e:
                print("Parse Error:", e)


# Start receive thread
threading.Thread(target=receive, daemon=True).start()

print("Listening for LoRa data...")
print("Type message and press ENTER to send\n")

# -------- SEND LOOP --------
while True:
    try:
        msg = input(">> ")
        ser.write((msg + "\n").encode())
    except KeyboardInterrupt:
        print("\nExiting...")
        break

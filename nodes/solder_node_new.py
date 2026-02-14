import serial
import threading
import json
import time

SERIAL_PORT = "COM3"
BAUD = 115200
OUTPUT_FILE = "data.json"

ser = serial.Serial(SERIAL_PORT, BAUD, timeout=0.1)

SOLDIER_ID = "soldier_01"

def update_json(message, lat, lon, heading, direction):

    data = {
        "id": SOLDIER_ID,
        "message": message,
        "location": {
            "latitude": lat,
            "longitude": lon
        },
        "heading": {
            "degrees": heading,
            "direction": direction
        },
        "timestamp": int(time.time())
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print("✅ JSON updated")
    print(data)


def receive():
    while True:
        try:
            line = ser.readline().decode(errors='ignore').strip()

            if not line:
                continue

            print("<<", line)

            if line.startswith("RX:[DATA]") or line.startswith("[DATA]"):

                payload = line.replace("RX:[DATA]", "").replace("[DATA]", "").strip()
                parts = payload.split("|")

                # -------- message --------
                message = parts[0].strip() if len(parts) >= 1 else ""

                # -------- GPS --------
                lat, lon = 0.0, 0.0
                if len(parts) >= 2 and "," in parts[1]:
                    try:
                        lat_str, lon_str = parts[1].split(",")
                        lat = float(lat_str)
                        lon = float(lon_str)
                    except:
                        pass

                # -------- heading (optional) --------
                heading = 0.0
                direction = "NA"
                if len(parts) >= 3 and "," in parts[2]:
                    try:
                        heading_str, direction = parts[2].split(",")
                        heading = float(heading_str)
                        direction = direction.strip()
                    except:
                        pass

                update_json(message, lat, lon, heading, direction)

        except Exception as e:
            print("Parse error:", e)


threading.Thread(target=receive, daemon=True).start()

print("Listening for LoRa data...")
print("Type message and press ENTER to send\n")

while True:
    try:
        msg = input(">> ")
        ser.write((msg + "\n").encode())
    except KeyboardInterrupt:
        break
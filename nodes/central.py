import serial
import threading
import json
import time

from decrypt_speech import decrypt_and_speak

SERIAL_PORT = "COM5"
BAUD = 115200
OUTPUT_FILE = "data.json"

ser = serial.Serial(SERIAL_PORT, BAUD, timeout=0.1)

SOLDIER_ID = "soldier_01"


def update_json(lat, lon, degrees, dists, health):
    data = {
        "id": SOLDIER_ID,
        "location": {"latitude": lat, "longitude": lon},
        "heading": degrees,
        "dists": dists,
        "health": health,
        "timestamp": int(time.time()),
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print("JSON file updated.")


def receive():
    while True:
        try:
            line = ser.readline().decode(errors="ignore").strip()

            if not line:
                continue
            print("<<", line)

            if line.startswith("[D]"):
                payload = line[3:].strip()

                try:
                    data, iv = payload.split(",", 1)
                    message = decrypt_and_speak(data, iv)
                    print(">> Decrypted Message:", message)
                except Exception as e:
                    print("Decrypt Error:", e)

            elif line.startswith("[S]"):
                payload = line[3:].strip()

                try:
                    gps_part, heading_part, dist, health = payload.split("|")

                    # GPS
                    lat_str, lon_str = gps_part.split(",")
                    lat = float(lat_str)
                    lon = float(lon_str)

                    # Heading (assuming single value like "123")
                    heading = float(heading_part)

                    # Distances
                    dists = list(map(float, dist.split(",")))

                    # Health
                    health = float(health)

                    update_json(lat, lon, heading, dists, health)

                except Exception as e:
                    print("Self Data Parse Error:", e)

        except Exception as e:
            print("Serial Error:", e)


# Start receiver thread
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

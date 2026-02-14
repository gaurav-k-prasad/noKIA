import serial
import threading
import json
import time

SERIAL_PORT = "COM5"
BAUD = 115200
OUTPUT_FILE = "data.json"

ser = serial.Serial(SERIAL_PORT, BAUD, timeout=0.1)

SOLDIER_ID = "soldier_01"

def update_json(message, lat, lon, degrees, direction):
    data = {
        "id": SOLDIER_ID,
        "message": message,
        "location": {
            "latitude": lat,
            "longitude": lon
        },
        "heading": {
            "degrees": degrees,
            "direction": direction
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

        if "[DATA]" in line:
            try:
                payload = line.split("[DATA]")[-1].strip()
                parts = payload.split("|")

                # message
                message = parts[0].strip()

                # gps
                lat, lon = 0.0, 0.0
                if len(parts) >= 2 and "," in parts[1]:
                    lat_str, lon_str = parts[1].strip().split(",")
                    lat = float(lat_str)
                    lon = float(lon_str)

                # heading (soldier only)
                degrees = 0.0
                direction = ""
                if len(parts) >= 3 and "," in parts[2]:
                    degree_str, direction = parts[2].strip().split(",")
                    degrees = float(degree_str)
                    direction = direction.strip()

                update_json(message, lat, lon, degrees, direction)

            except Exception as e:
                print("Parse Error:", e)


# Start receiver thread
threading.Thread(target=receive, daemon=True).start()

print("Listening for LoRa data...")
print("USAGE:")
print("  text only → Hello")
print("  gps only → /gps |12.97,77.59")
print("  text + gps → /gps Move|12.97,77.59\n")


# -------- SEND LOOP --------
while True:
    try:
        msg = input(">> ").strip()

        # 🔹 GPS MODE (manual)
        if msg.lower().startswith("/gps"):
            payload = msg[4:].strip()

            # If user sends only coordinates
            if payload.startswith("|"):
                payload = " " + payload  # empty message allowed

            if "|" not in payload:
                print("Format: /gps message|lat,lon")
                continue

            tx_packet = f"[DATA]{payload}\n"
            ser.write(tx_packet.encode())
            print(">> SENT:", tx_packet.strip())

        # 🔹 TEXT ONLY MODE
        else:
            tx_packet = f"[DATA]{msg}|0.0,0.0\n"
            ser.write(tx_packet.encode())
            print(">> SENT:", tx_packet.strip())

    except KeyboardInterrupt:
        print("\nExiting...")
        break

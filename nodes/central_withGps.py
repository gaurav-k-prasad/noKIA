import os
import serial
import threading
import json
import time

from decrypt_speech import decrypt_and_speak

SERIAL_PORT = "COM5"
BAUD = 115200
OUTPUT_FILE = "data.json"
new_lat, new_lng = 0, 0

ser = serial.Serial(SERIAL_PORT, BAUD, timeout=0.1)

SOLDIER_ID = "soldier_01"


def update_json(lat, lon, degrees, heart):
    data = {
        "id": SOLDIER_ID,
        "location": {"latitude": lat, "longitude": lon},
        "degrees": degrees,
        "heart": heart,
        "timestamp": int(time.time()),
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print("JSON file updated.")


def receive():
    while True:
        line = ser.readline().decode(errors="ignore").strip()

        if not line:
            print("no line")
            continue

        print("line", line)

        if "[D]" in line:
            try:
                payload = line.split("[D]")[-1]
                data, iv = payload.split(",")
                message = decrypt_and_speak(data, iv)

            except Exception as e:
                print("Parse Error:", e)
        elif "[S]" in line:
            payload = line.split("[S]")[-1]
            latlan, heading, dists, heart = payload.split("|")

            lat, lon = list(map(int, latlan.split(",")))
            heading = int(heading)
            dists = map(int, dists.split(","))
            heart = int(heart)
            update_json(lat, lon, heading, heart)


def watch_voice_queue():
    while True:
        if os.path.exists("temp_message.json"):
            try:
                with open("temp_message.json", "r") as f:
                    encrypted_data = json.load(f)

                isData = encrypted_data.get("valid", False)

                if isData:
                    payload = encrypted_data["data"] + "," + encrypted_data["iv"]
                    tx_packet = f"[D]{payload}\n"
                    ser.write(tx_packet.encode())
                    print("\n>> AUTO-SENT ENCRYPTED VOICE PACKET")

                    with open("temp_message.json", "w") as f:
                        json.dump({"valid": False}, f)

            except Exception as e:
                print("Queue Error:", e)

        time.sleep(1)


t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=watch_voice_queue)

t1.start()
t2.start()

t1.join()
t2.join()

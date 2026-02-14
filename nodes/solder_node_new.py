import os
import serial
import threading
import json
import time
from decrypt_speech import decrypt_and_speak
import visionrpi as vision  # module for cv

SERIAL_PORT = "COM3"
BAUD = 115200
OUTPUT_FILE = "data.json"

ser = serial.Serial(SERIAL_PORT, BAUD, timeout=0.1)

SOLDIER_ID = "soldier_01"


def update_json(message):

    data = {"id": SOLDIER_ID, "message": message, "timestamp": int(time.time())}

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print("✅ JSON updated")
    print(data)


def receive():
    while True:
        try:
            line = ser.readline().decode(errors="ignore").strip()
            if not line:
                continue

            if line.startswith("[D]"):
                try:
                    payload = line.replace("[D]", "").strip()
                    data, iv = payload.split(",")
                    message = decrypt_and_speak(data, iv)
                    update_json(message)

                except Exception as e:
                    print("Parse Error:", e)
        except Exception as e:
            print("Parse error:", e)


def watch_voice_queue():
    while True:
        if os.path.exists("temp_message.json"):
            try:
                with open("temp_message.json", "w") as f:
                    encrypted_data = json.load(f)
                    isData = encrypted_data["valid"]

                    if isData:
                        payload = encrypted_data["data"] + "," + encrypted_data["iv"]
                        tx_packet = f"[D]{payload}\n"
                        ser.write(tx_packet.encode())
                        print("\n>> AUTO-SENT ENCRYPTED VOICE PACKET")
                        json.dump({"valid": False}, f)

            except Exception as e:
                print("Queue Error:", e)

        time.sleep(1)


def send_self_data():
    while True:
        # ! WARNING
        payload = "12,55" + "|" + "123" + "|" + vision.get_data() + "|" + "32"
        tx_packet = f"[S]{payload}\n"
        ser.write(tx_packet.encode())
        print("\n>> AUTO-SENT LAT LNG")

        time.sleep(3)


threading.Thread(target=receive, daemon=True).start()
threading.Thread(target=watch_voice_queue, daemon=True).start()
threading.Thread(target=send_self_data, daemon=True).start()

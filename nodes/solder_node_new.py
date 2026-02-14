import os
import serial
import threading
import json
import time
from decrypt_speech import decrypt_and_queue

# import visionrpi as vision  # module for cv

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
                print("no output")
                continue
            print("line", line)

            if "[D]" in line:
                try:
                    payload = line.split("[D]")[-1].strip()
                    data, iv = payload.split(",")

                    message = decrypt_and_queue(data, iv)
                    update_json(message)


                except Exception as e:
                    print("Parse Error:", e)
        except Exception as e:
            print("Parse error:", e)


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


def send_self_data():
    while True:
        # ! WARNING
        payload = "12,55" + "|" + "123" + "|" + "53,33,22" + "|" + "32"
        tx_packet = f"[S]{payload}\n"
        ser.write(tx_packet.encode())
        print("\n>> AUTO-SENT LAT LNG")

        time.sleep(3)


t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=watch_voice_queue)
t3 = threading.Thread(target=send_self_data)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

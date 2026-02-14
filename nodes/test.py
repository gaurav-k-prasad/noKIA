import serial
import time

# 1. Update 'COM3' to your actual port (e.g., 'COM5' or '/dev/ttyUSB0')
# 2. Match the baud rate exactly (115200)
try:
    ser = serial.Serial("COM3", 115200, timeout=1)
    time.sleep(2)  # Give the ESP32 time to reboot after connection
    print("Connected to ESP32...")
except Exception as e:
    print(f"Error opening serial port: {e}")
    exit()

while True:
    try:
        if ser.in_waiting > 0:
            # Read the raw bytes and decode to string
            raw_data = ser.readline()
            line = raw_data.decode("utf-8").strip()

            if line:
                print(f"Received: {line}")

                # Logic to parse your [S]lat,lng|heading format
                if line.startswith("[S]"):
                    # Remove the [S] tag and split by |
                    clean_data = line.replace("[S]", "")
                    parts = clean_data.split("|")

                    if len(parts) == 2:
                        coords = parts[0]  # "lat,lng"
                        heading = parts[1]  # "heading"
                        print(f"  -> GPS: {coords} | Compass: {heading}")

    except KeyboardInterrupt:
        print("Closing program...")
        ser.close()
        break
    except Exception as e:
        print(f"Data error: {e}")

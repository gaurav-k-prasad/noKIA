import serial
import threading

SERIAL_PORT = "COM5"   # Change per laptop
BAUD = 115200

ser = serial.Serial(SERIAL_PORT, BAUD, timeout=0.1)

# -------- RECEIVE THREAD --------
def receive():
    while True:
        line = ser.readline().decode(errors='ignore').strip()
        if line:
            print("<<", line)

# Start receiver
threading.Thread(target=receive, daemon=True).start()

print("Type message and press ENTER to send")

# -------- SEND LOOP --------
while True:
    msg = input(">> ")
    ser.write((msg + "\n").encode())
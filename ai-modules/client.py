import socket
import sounddevice as sd

HOST = "127.0.0.1"
PORT = 5000

SAMPLE_RATE = 16000
DURATION = 5  # seconds


print("Recording... Speak now")

recording = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="int16"
)

sd.wait()

print(" Sending packets...")

client = socket.socket()
client.connect((HOST, PORT))

client.sendall(recording.tobytes())

client.close()

print(" Data sent")

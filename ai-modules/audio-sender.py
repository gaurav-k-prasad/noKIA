"""import socket
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
"""

import sounddevice as sd
import numpy as np
import board
import busio
import digitalio
import adafruit_rfm9x
import time

# --- LORA HARDWARE SETUP ---
# Configure these pins based on your specific LoRa HAT
CS = digitalio.DigitalInOut(board.CE1)
RESET = digitalio.DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialize LoRa module (Change 915.0 to 868.0 if you are in Europe/India)
try:
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
    print("LoRa radio initialized successfully!")
except RuntimeError as error:
    print(f"LoRa error: {error}. Check your wiring.")
    exit()

# --- AUDIO SETUP ---
SAMPLE_RATE = 8000  # Downsampled for LoRa
DURATION = 1        # Keep it to 1 second. Anything more will take forever.

print("\nRecording 1 second of audio... Speak now!")
# Record as int8 (1 byte per sample) to halve the data size
recording = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="int8"
)
sd.wait()

# Convert numpy array to raw bytes
audio_data = recording.tobytes()
print(f"Recorded {len(audio_data)} bytes. Preparing to send over LoRa...\n")

# --- TRANSMISSION ---
CHUNK_SIZE = 240  # Safely below LoRa's 252-byte payload limit
total_chunks = (len(audio_data) + CHUNK_SIZE - 1) // CHUNK_SIZE

for i in range(0, len(audio_data), CHUNK_SIZE):
    chunk = audio_data[i:i+CHUNK_SIZE]
    
    # Send the packet
    rfm9x.send(chunk)
    
    chunk_num = (i // CHUNK_SIZE) + 1
    print(f"Sent chunk {chunk_num} of {total_chunks}...")
    
    # Tiny sleep to allow the radio buffer to clear and respect duty cycles
    time.sleep(0.05) 

print("\nAll audio data sent over LoRa!")
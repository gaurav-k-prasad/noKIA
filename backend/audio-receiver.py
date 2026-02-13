"""import socket
import wave
import speech_recognition as sr

HOST = "0.0.0.0"
PORT = 5000
SAMPLE_RATE = 16000

server = socket.socket()
server.bind((HOST, PORT))
server.listen(1)

print(" Server waiting...")

conn, addr = server.accept()
print(" Connected:", addr)

frames = []

while True:
    data = conn.recv(4096)

    if not data:
        break

    frames.append(data)

conn.close()
server.close()

print(" Saving audio...")

filename = "received.wav"

with wave.open(filename, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(b"".join(frames))

def convert_to_text(wav_file):
    r = sr.Recognizer()

    with sr.AudioFile(wav_file) as source:
        audio = r.record(source)

    try:
        text = r.recognize_google(audio)
        return text
    except:
        return "Could not recognize speech"

text = convert_to_text(filename)

print(" FINAL TEXT:", text)
"""

import board
import busio
import digitalio
import adafruit_rfm9x
import sounddevice as sd
import numpy as np

# --- LORA HARDWARE SETUP ---
CS = digitalio.DigitalInOut(board.CE1)
RESET = digitalio.DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
print("Receiver listening for LoRa packets...\n")

SAMPLE_RATE = 8000
EXPECTED_CHUNKS = 34  # 8000 bytes / 240 bytes per chunk

received_audio = bytearray()
chunks_received = 0

while True:
    # Wait for a packet
    packet = rfm9x.receive(timeout=5.0)

    if packet is not None:
        received_audio.extend(packet)
        chunks_received += 1
        print(f"Received chunk {chunks_received}/{EXPECTED_CHUNKS}")

        # If we've received enough data to make roughly 1 second of audio
        if chunks_received >= EXPECTED_CHUNKS:
            print("\nAudio file assembled! Playing now...")

            # Convert bytes back to numpy array and play
            audio_array = np.frombuffer(received_audio, dtype=np.int8)
            sd.play(audio_array, samplerate=SAMPLE_RATE)
            sd.wait()

            # Reset for the next message
            received_audio = bytearray()
            chunks_received = 0
            print("\nListening for next message...")

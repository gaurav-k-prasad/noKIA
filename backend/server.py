import socket
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


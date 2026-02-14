import json
import base64
import speech_recognition as sr
import keyboard
import time

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256

PASSWORD = "my_secret_key_123"


def get_key(password):
    return SHA256.new(password.encode()).digest()


def encrypt_aes(text, key):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(text.encode(), AES.block_size))
    return encrypted, iv


recognizer = sr.Recognizer()

print("\n Hold SPACE to talk (say 'exit' to quit)\n")

while True:
    print("Waiting for SPACE...")

    keyboard.wait("space")
    print("Listening... (release SPACE to stop)")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)

        audio_chunks = []
        sample_rate = source.SAMPLE_RATE
        sample_width = source.SAMPLE_WIDTH

        # record continuously while space is held
        while keyboard.is_pressed("space"):
            try:
                chunk = recognizer.record(source, duration=0.3)
                audio_chunks.append(chunk.get_raw_data())
            except Exception:
                pass

    if not audio_chunks:
        continue

    # combine all recorded audio
    full_audio = sr.AudioData(b"".join(audio_chunks), sample_rate, sample_width)

    try:
        text = recognizer.recognize_google(full_audio)
        print("\n Recognized Text:")
        print(text)

        if text.lower() == "exit":
            break

        obj = {"message": text}

        key = get_key(PASSWORD)
        enc, iv = encrypt_aes(json.dumps(obj), key)

        output = {
            "data": base64.b64encode(enc).decode(),
            "iv": base64.b64encode(iv).decode(),
            "valid": True,
        }

        # dump to a temp file
        with open("temp_message.json", "w") as f:
            json.dump(output, f, indent=2)

        print("\n Encrypted Output:")
        print(json.dumps(output, indent=2))
        print("\n----------------------------------\n")

    except sr.UnknownValueError:
        print(" Could not understand audio")

    except sr.RequestError:
        print(" Internet error")

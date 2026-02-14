import json
import base64
import speech_recognition as sr

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

print("\n Speak something (say 'exit' to quit)\n")

while True:
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
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
            "valid": True
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
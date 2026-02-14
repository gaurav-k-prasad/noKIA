import pyttsx3
import json
import base64
import queue
import threading

engine = pyttsx3.init()
engine.setProperty("rate", 170)
speech_queue = queue.Queue()


from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Hash import SHA256


# =====================
# AES PASSWORD
# =====================
PASSWORD = "my_secret_key_123"


def get_key(password):
    return SHA256.new(password.encode()).digest()


def decrypt_aes(enc_data, iv, key):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(enc_data)

    return unpad(decrypted, AES.block_size).decode()


def decrypt_message(enc_b64, iv_b64):
    """
    Decrypts Base64 encoded ciphertext + IV
    Returns plaintext message
    """
    try:
        enc_bytes = base64.b64decode(enc_b64)
        iv_bytes = base64.b64decode(iv_b64)

        key = get_key(PASSWORD)
        decrypted_text = decrypt_aes(enc_bytes, iv_bytes, key)

        try:
            parsed_json = json.loads(decrypted_text)
            return parsed_json.get("message", decrypted_text)
        except json.JSONDecodeError:
            return decrypted_text

    except Exception as e:
        print("Decryption Error:", e)
        return None


def speak_text(text):
    """
    Speaks text safely (called only by worker)
    """
    if text:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("Speech Error:", e)


def speech_worker():
    while True:
        text = speech_queue.get()

        if text is None:
            break  # graceful shutdown

        speak_text(text)

        speech_queue.task_done()


def decrypt_and_queue(enc_b64, iv_b64):
    """
    Decrypts message and queues for speech
    """
    message = decrypt_message(enc_b64, iv_b64)

    if message:
        print("Decrypted:", message)
        speech_queue.put(message)

    return message

threading.Thread(target=speech_worker, daemon=True).start()


def decrypt_and_speak(enc_b64, iv_b64):
    """
    Takes Base64 encoded ciphertext and IV, decrypts using global password,
    and speaks the resulting message.
    """
    enc_bytes = base64.b64decode(enc_b64)
    iv_bytes = base64.b64decode(iv_b64)

    key = get_key(PASSWORD)
    decrypted_text = decrypt_aes(enc_bytes, iv_bytes, key)

    try:
        parsed_json = json.loads(decrypted_text)
        message_to_speak = parsed_json.get("message", decrypted_text)
    except json.JSONDecodeError:
        message_to_speak = decrypted_text

    if message_to_speak:
        engine.say(message_to_speak)
        engine.runAndWait()

    return message_to_speak

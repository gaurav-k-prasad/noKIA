import pyttsx3
import json
import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Hash import SHA256


# 🔑 SAME PASSWORD AS encrypt.py
PASSWORD = "my_secret_key_123"


def get_key(password):
    return SHA256.new(password.encode()).digest()


def decrypt_aes(enc_data, iv, key):

    cipher = AES.new(key, AES.MODE_CBC, iv)

    decrypted = cipher.decrypt(enc_data)

    return unpad(decrypted, AES.block_size).decode()


# =====================
# Text To Speech
# =====================
engine = pyttsx3.init()
engine.setProperty("rate", 170)


print("\nPaste ENCRYPTED JSON")
print("Type exit to quit\n")


while True:

    data = input("JSON> ")

    if data.lower() == "exit":
        break

    try:
        # Read encrypted JSON
        obj = json.loads(data)

        enc_b64 = obj["data"]
        iv_b64 = obj["iv"]

        enc_bytes = base64.b64decode(enc_b64)
        iv_bytes = base64.b64decode(iv_b64)

        key = get_key(PASSWORD)

        # Decrypt
        decrypted_text = decrypt_aes(enc_bytes, iv_bytes, key)

        print("\n🔓 Decrypted JSON:")
        print(decrypted_text)

        # Convert to JSON
        plain_obj = json.loads(decrypted_text)

        # Get message
        msg = plain_obj.get("message", "")

        if msg:
            print("\n🔊 Speaking:", msg)

            engine.say(msg)
            engine.runAndWait()
        else:
            print("❌ No 'message' found")

    except Exception as e:
        print("❌ Error:", e)

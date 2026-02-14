import pyttsx3
import json
import base64

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


# =====================
# Text To Speech
# =====================
engine = pyttsx3.init()
engine.setProperty("rate", 170)


print("\n Paste ENCRYPTED JSON (Multi-line supported)")
print("Just press Enter after last } \n")


while True:

    lines = []
    open_braces = 0

    # Read until JSON complete
    while True:

        line = input()

        open_braces += line.count("{")
        open_braces -= line.count("}")

        lines.append(line)

        # JSON finished
        if open_braces == 0 and "{" in "".join(lines):
            break

    data = "\n".join(lines).strip()

    if data.lower() == "exit":
        break

    try:
        # Parse encrypted JSON
        obj = json.loads(data)

        enc_b64 = obj["data"]
        iv_b64 = obj["iv"]

        enc_bytes = base64.b64decode(enc_b64)
        iv_bytes = base64.b64decode(iv_b64)

        key = get_key(PASSWORD)

        # 🔓 Decrypt
        decrypted_text = decrypt_aes(enc_bytes, iv_bytes, key)

        print("\n Decrypted JSON:")
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
            print(" No 'message' found")

        print("\n📄 Paste next encrypted JSON...\n")

    except Exception as e:
        print("\n Error:")
        print(e)
        print("\nTry again.\n")

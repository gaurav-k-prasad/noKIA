import json
import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256


# 🔑 Must be SAME in both files
PASSWORD = "my_secret_key_123"


def get_key(password):
    return SHA256.new(password.encode()).digest()


def encrypt_aes(text, key):

    iv = get_random_bytes(16)

    cipher = AES.new(key, AES.MODE_CBC, iv)

    encrypted = cipher.encrypt(pad(text.encode(), AES.block_size))

    return encrypted, iv


print("\nPaste NORMAL JSON")
print("Type exit to quit\n")


while True:

    data = input("JSON> ")

    if data.lower() == "exit":
        break

    try:
        # Parse JSON
        obj = json.loads(data)

        key = get_key(PASSWORD)

        # Encrypt
        enc, iv = encrypt_aes(json.dumps(obj), key)

        output = {
            "data": base64.b64encode(enc).decode(),
            "iv": base64.b64encode(iv).decode()
        }

        print("\n🔐 Encrypted JSON (Send this):")
        print(json.dumps(output, indent=2))

    except Exception as e:
        print("❌ Error:", e)

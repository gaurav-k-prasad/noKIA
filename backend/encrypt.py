import json
import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256


# ==========================
# AES PASSWORD (same everywhere)
# ==========================
PASSWORD = "my_secret_key_123"


def get_key(password):
    return SHA256.new(password.encode()).digest()


def encrypt_aes(text, key):

    iv = get_random_bytes(16)

    cipher = AES.new(key, AES.MODE_CBC, iv)

    encrypted = cipher.encrypt(pad(text.encode(), AES.block_size))

    return encrypted, iv


print("\n Paste NORMAL JSON (Multi-line supported)")
print("Just press Enter after last } \n")


while True:

    lines = []
    open_braces = 0

    # Read until JSON is complete
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
        # Validate JSON
        obj = json.loads(data)

        key = get_key(PASSWORD)

        # Encrypt
        enc, iv = encrypt_aes(json.dumps(obj), key)

        output = {
            "data": base64.b64encode(enc).decode(),
            "iv": base64.b64encode(iv).decode()
        }

        print("\n🔐 Encrypted JSON (Send this):\n")
        print(json.dumps(output, indent=2))

        print("\n📄 Paste next JSON...\n")

    except Exception as e:
        print("\n Error:")
        print(e)
        print("\nTry again.\n")

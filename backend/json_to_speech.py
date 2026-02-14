import pyttsx3
import json

engine = pyttsx3.init()
engine.setProperty('rate', 170)

print("Paste your JSON (single line) and press Enter:")
print("Type exit to quit\n")

while True:

    data = input("JSON> ")

    if data.lower() == "exit":
        break

    try:
        obj = json.loads(data)

        # Extract message
        text = obj.get("message", "")

        if not text:
            print(" No 'message' field found")
            continue

        print("Speaking:", text)

        engine.say(text)
        engine.runAndWait()

    except json.JSONDecodeError:
        print(" Invalid JSON format")

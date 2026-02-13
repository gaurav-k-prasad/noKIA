import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:

    print(" Speak now...")

    r.adjust_for_ambient_noise(source)

    audio = r.listen(source)

    print("Processing...")

    try:
        text = r.recognize_google(audio)

        print(" You said:", text)

    except sr.UnknownValueError:
        print("Could not understand")

    except sr.RequestError:
        print("Internet error")

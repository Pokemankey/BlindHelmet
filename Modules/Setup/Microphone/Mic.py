import speech_recognition as sr

def getUserInput():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                print("")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))
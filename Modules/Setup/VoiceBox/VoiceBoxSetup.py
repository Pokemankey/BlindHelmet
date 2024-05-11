from gtts import gTTS
import os
from playsound import playsound

def speak(sentence):
    tts = gTTS(text=sentence, lang="en", slow=False)
    tts.save("voice.mp3")
    playsound("voice.mp3")
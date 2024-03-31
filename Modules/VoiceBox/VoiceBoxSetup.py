import pyttsx3

def set_jarvis_voice(engine):
    # Get list of available voices
    voices = engine.getProperty('voices')
    # Find a voice that is closest to J.A.R.V.I.S. (this is just an approximation)
    for voice in voices:
        if "Microsoft David Desktop - English (United States)" in voice.name:
            engine.setProperty('voice', voice.id)
            break


def getVoiceBox():
    #Jarvis voice setup
    engine = pyttsx3.init()
    set_jarvis_voice(engine)
    engine.setProperty('rate', 180)  # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

    return engine


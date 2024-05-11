import json
import google.generativeai as genai
from API_KEYS import GOOGLE_API_KEY

from Modules.Setup.VoiceBox.VoiceBoxSetup import getVoiceBox
from Modules.Setup.Microphone.Mic import getUserInput

def askGeminiQuestion():
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        engine = getVoiceBox()
        confirm = True
        userInput = ""


        while True:
            engine.say("What do you want to ask me?")
            engine.runAndWait()
            userInput = getUserInput()
            engine.say(f"Did You Ask {userInput}")
            engine.runAndWait()
            confirm = getUserInput()
            if "yes" in confirm.lower():
                break

        response = model.generate_content(userInput + " in a max of 5 sentences")
        engine.say(response.text)
        engine.runAndWait()
        engine.say("Exiting to main menu")
        engine.runAndWait()
    except Exception as e:
        engine.say("Error Occured , No wifi available or api key missing")
        engine.runAndWait()

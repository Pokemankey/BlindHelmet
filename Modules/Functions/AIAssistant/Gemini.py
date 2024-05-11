import json
import google.generativeai as genai
from API_KEYS import GOOGLE_API_KEY

from Modules.Setup.VoiceBox.VoiceBoxSetup import speak
from Modules.Setup.Microphone.Mic import getUserInput

def askGeminiQuestion():
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        confirm = True
        userInput = ""


        while True:
            speak("What do you want to ask me?")
            userInput = getUserInput()
            speak(f"Did You Ask {userInput}")
            confirm = getUserInput()
            if "yes" in confirm.lower():
                break

        response = model.generate_content(userInput + " in a max of 5 sentences")
        speak(response.text)
        speak("Exiting to main menu")
        
    except Exception as e:
        speak("Error Occured , No wifi available or api key missing")
        

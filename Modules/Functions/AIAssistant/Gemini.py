import json
import google.generativeai as genai
from API_KEYS import GOOGLE_API_KEY

from Modules.Setup.VoiceBox.VoiceBoxSetup import getVoiceBox

def askGeminiQuestion(recognizer, stream):

    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        engine = getVoiceBox()
        confirm = True
        userInput = ""
        while True:
            if confirm: 
                engine.say("What do you want to ask me?")
                engine.runAndWait()
                confirm = False
            data = stream.read(2000)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                resultMap = json.loads(result.lower())
                print(resultMap['text'])
                engine.say("is this what you asked me " + resultMap['text'])
                engine.runAndWait()
                while True:
                    data2 = stream.read(2000)
                    if recognizer.AcceptWaveform(data2):
                        result1 = recognizer.Result()
                        resultMap1 = json.loads(result1.lower())
                        if "yes"  in resultMap1['text']:
                            userInput = resultMap['text']
                            break
                        elif "no"  in resultMap1['text']:
                            confirm = True
                            break
                if not confirm:
                    break
                        
        response = model.generate_content(userInput + " in a max of 5 sentences")
        engine.say(response.text)
        engine.runAndWait()
        engine.say("Exiting to main menu")
        engine.runAndWait()
    except Exception as e:
        engine.say("Error Occured , No wifi available or api key missing")
        engine.runAndWait()

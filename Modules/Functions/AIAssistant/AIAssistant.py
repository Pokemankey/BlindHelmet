import json
import google.generativeai as genai
from API_KEYS import GOOGLE_API_KEY

from Modules.Setup.Config.config import AiName
from Modules.Setup.VoiceBox.VoiceBoxSetup import getVoiceBox
from Modules.Setup.Config.Commands import ValidCommand,evaluateInput

def get_ai_assistant(recognizer, stream, nlpModel, tfidf_vectorizer):

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    
    while True:
        engine = getVoiceBox()

        booli = True
        booli2 = True
        userInput = ""
        while True:
            if booli2: 
                engine.say("What do you want to ask me?")
                engine.runAndWait()
                booli2 = False
            data = stream.read(2000)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                resultMap = json.loads(result.lower())
                print(resultMap['text'])
                engine.say("is this what you asked me " + resultMap['text'])
                engine.runAndWait()
                while booli:
                    data2 = stream.read(2000)
                    if recognizer.AcceptWaveform(data2):
                        result1 = recognizer.Result()
                        resultMap1 = json.loads(result1.lower())
                        if "yes"  in resultMap1['text']:
                            userInput = resultMap['text']
                            booli = False
                            break
                        elif "no"  in resultMap1['text']:
                            booli2 = True
                            break
                if not booli:
                    break
                        



        response = model.generate_content(userInput + " in a max of two sentences")
        engine.say(response.text)
        engine.runAndWait()
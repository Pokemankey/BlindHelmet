from vosk import Model, KaldiRecognizer
import pyaudio
import json
import google.generativeai as genai
#Module Imports
from Modules.Setup.Config.config import SpeechRecognitionModelPath,MicrophoneIndex
from Modules.Setup.Config.config import AiName
from Modules.Setup.Camera.CameraSetup import getCamera
from Modules.Setup.VoiceBox.VoiceBoxSetup import getVoiceBox

from Modules.Setup.Config.Commands import getNLPModel,getTfidfVectorizer,evaluateInput,ValidCommand

from Modules.Functions.Detection.OCR.OCR_Setup import OCR_Setup
from Modules.Functions.Detection.ObjectDetection.ObjectDetection import ObjectDetection
from Modules.Functions.Detection.HumanDetection.HumanDetection import HumanDetection
from Modules.Functions.AIAssistant.AIAssistant import get_ai_assistant
from Modules.Functions.YoutubePlayer.YoutubePlayer import YoutubePlayer
from Modules.Functions.Weather.FetchWeather import get_weather_forecast
from Modules.Functions.DateAndTime.fetchDateAndTime import get_current_datetime
from Modules.Functions.Help.Help import getHelp

from API_KEYS import GOOGLE_API_KEY

def FindCommand(cap,text,nlpModel,tfidf_vectorizer,recognizer,stream):
    get_ai_assistant(recognizer,stream,nlpModel,tfidf_vectorizer)
    # output = evaluateInput(text,nlpModel,tfidf_vectorizer)
    # print(f"Running {output}")
    # if output == "OCR":
    #     OCR_Setup(cap)
    # elif output == "ObjectDetection":
    #     ObjectDetection(cap)
    # elif output == "HumanDetection":
    #     HumanDetection(cap)
    # elif output == "Youtube":
    #     YoutubePlayer(recognizer,stream,nlpModel,tfidf_vectorizer)
    # elif output == "WeatherLookup":
    #     get_weather_forecast()
    # elif output == "Date":
    #     get_current_datetime()
    # elif output == "AI":
    #     get_ai_assistant(recognizer,stream,nlpModel,tfidf_vectorizer)
    # elif output == "Help":
    #     getHelp()

    


def Jarvis():
    #Camera Setup
    cap = getCamera()

    #microphone setup
    model = Model(SpeechRecognitionModelPath)
    recognizer = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2000,
                    input_device_index=MicrophoneIndex)
    #NLP setup
    nlpModel = getNLPModel()
    tfidf_vectorizer = getTfidfVectorizer()

    #Voice Module Setup
    engine = getVoiceBox()
    engine.say(f"{AiName} online")
    engine.runAndWait()

    while True:
        data = stream.read(2000)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            resultMap = json.loads(result.lower())
            print(resultMap["text"])
            if ValidCommand(resultMap["text"]):
                command = resultMap["text"].replace("zero ", "")
                FindCommand(cap,command,nlpModel,tfidf_vectorizer,recognizer,stream)

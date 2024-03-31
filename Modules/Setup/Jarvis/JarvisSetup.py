from vosk import Model, KaldiRecognizer
import pyaudio
import json
#Module Imports
from Modules.Setup.Config.config import SpeechRecognitionModelPath,MicrophoneIndex
from Modules.Setup.Config.config import AiName
from Modules.Setup.Camera.CameraSetup import getCamera
from Modules.Setup.VoiceBox.VoiceBoxSetup import getVoiceBox

from Modules.Setup.Config.Commands import getNLPModel,getTfidfVectorizer,evaluateInput,ValidCommand


from Modules.Functions.Detection.OCR.OCR_Setup import OCR_Setup
from Modules.Functions.Detection.ObjectDetection.ObjectDetection import ObjectDetection
from Modules.Functions.Detection.HumanDetection.HumanDetection import HumanDetection
from Modules.Functions.Weather.FetchWeather import get_weather_forecast


def FindCommand(cap,text,nlpModel,tfidf_vectorizer):
    output = evaluateInput(text,nlpModel,tfidf_vectorizer)
    print(f"Running {text}")
    if output == "OCR":
        OCR_Setup(cap)
    elif output == "ObjectDetection":
        ObjectDetection(cap)
    elif output == "HumanDetection":
        HumanDetection(cap)
    elif output == "WeatherLookup":
        get_weather_forecast()
    


def Jarvis():
    #Camera Setup
    cap = getCamera()

    #microphone setup
    model = Model(SpeechRecognitionModelPath)
    recognizer = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    device_index = MicrophoneIndex 
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000,
                    input_device_index=device_index)
    #NLP setup
    nlpModel = getNLPModel()
    tfidf_vectorizer = getTfidfVectorizer()

    #Voice Module Setup
    engine = getVoiceBox()
    engine.say(f"{AiName} online")
    engine.runAndWait()

    while True:
        data = stream.read(8000)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            resultMap = json.loads(result.lower())
            if ValidCommand(resultMap["text"]):
                FindCommand(cap,resultMap["text"],nlpModel,tfidf_vectorizer)

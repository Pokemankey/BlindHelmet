from vosk import Model, KaldiRecognizer
import pyaudio
import json
import google.generativeai as genai
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

#Module Imports
from Modules.Setup.Config.config import SpeechRecognitionModelPath,MicrophoneIndex
from Modules.Setup.Config.config import AiName
from Modules.Setup.Camera.CameraSetup import getCamera
from Modules.Setup.VoiceBox.VoiceBoxSetup import getVoiceBox

from Modules.Setup.Config.Commands import evaluateInput,ValidCommand,ValidGeminiCommand

from Modules.Functions.Detection.OCR.OCR_Setup import OCR_Setup
from Modules.Functions.Detection.ObjectDetection.ObjectDetection import ObjectDetection
from Modules.Functions.Detection.HumanDetection.HumanDetection import HumanDetection
from Modules.Functions.Detection.FaceDetection.FaceDetection import saveFace,precompute_embeddings,detectFace
from Modules.Functions.AIAssistant.Gemini import askGeminiQuestion
from Modules.Functions.YoutubePlayer.YoutubePlayer import YoutubePlayer
from Modules.Functions.Weather.FetchWeather import get_weather_forecast
from Modules.Functions.DateAndTime.fetchDateAndTime import get_current_datetime
from Modules.Functions.Help.Help import getHelp

def FindCommand(text,db,recognizer,stream):
    global known_faces
    output = evaluateInput(text,db)
    print(f"Running {output}")
    if output == "OCR":
        OCR_Setup()
    elif output == "ObjectDetection":
        ObjectDetection()
    elif output == "HumanDetection":
        HumanDetection()
    elif output == "Youtube":
        YoutubePlayer(recognizer,stream,db)
    elif output == "WeatherLookup":
        get_weather_forecast()
    elif output == "Date":
        get_current_datetime()
    elif output == "Help":
        getHelp()
    elif output == "SaveFace":
        saveFace(recognizer,stream)
        known_faces = precompute_embeddings()
    elif output == "DetectFace":
        detectFace(known_faces)

def FindGeminiCommand(text,db,recognizer,stream):
    output = evaluateInput(text,db)
    # print(f"Running {output}")
    if output == "Gemini":
        askGeminiQuestion(recognizer,stream)

def Jarvis():
    global known_faces

    #microphone setup
    model = Model(SpeechRecognitionModelPath)
    recognizer = KaldiRecognizer(model, 48000)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=48000, input=True, frames_per_buffer=2000,
                    input_device_index=MicrophoneIndex)
    #Embeddings setup
    embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
    db = Chroma(
        embedding_function=embeddings,
        persist_directory="emb"
    )

    #Face database embeddings
    known_faces = precompute_embeddings()

    #Voice Module Setup
    engine = getVoiceBox()
    engine.say(f"{AiName} online")
    engine.runAndWait()

    while True:
        data = stream.read(2000,exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            resultMap = json.loads(result.lower())
            print(resultMap["text"])
            if ValidCommand(resultMap["text"]):
                command = resultMap["text"].replace("zero ", "")
                FindCommand(command,db,recognizer,stream)
            elif ValidGeminiCommand(resultMap["text"]):
                command = resultMap["text"]
                FindGeminiCommand(command,db,recognizer,stream)

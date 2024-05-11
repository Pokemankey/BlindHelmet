import google.generativeai as genai
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from ultralytics import YOLO
from doctr.models import ocr_predictor

#Module Imports
from Modules.Setup.Config.config import CocoModelPath,AiName
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

import speech_recognition as sr

def FindCommand(text,db,detectionModel,OCRmodel):
    global known_faces
    output = evaluateInput(text,db)
    print(f"Running {output}")
    if output == "OCR":
        OCR_Setup(OCRmodel)
    elif output == "ObjectDetection":
        ObjectDetection(detectionModel)
    elif output == "HumanDetection":
        HumanDetection(detectionModel)
    elif output == "Youtube":
        YoutubePlayer(db)
    elif output == "WeatherLookup":
        get_weather_forecast()
    elif output == "Date":
        get_current_datetime()
    elif output == "Help":
        getHelp()
    elif output == "SaveFace":
        saveFace()
        known_faces = precompute_embeddings()
    elif output == "FacialRecognition":
        detectFace(known_faces)

def FindGeminiCommand(text,db):
    output = evaluateInput(text,db)
    if output == "Gemini":
        askGeminiQuestion()

def Jarvis():
    global known_faces

    #microphone setup
    recognizer = sr.Recognizer()
    #Embeddings setup
    embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
    db = Chroma(
        embedding_function=embeddings,
        persist_directory="emb"
    )

    #Face database embeddings
    known_faces = precompute_embeddings()

    #Load detection Model
    detectionModel = YOLO(CocoModelPath)

    #Voice Module Setup
    engine = getVoiceBox()
    engine.say(f"{AiName} online")
    engine.runAndWait()

    #OCR Model
    OCRmodel = ocr_predictor(pretrained=True)


    while True:
        with sr.Microphone() as source:
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                if text:
                    print(text)
                    if ValidCommand(text):
                        command = text.replace("zero ", "")
                        FindCommand(command,db,detectionModel,OCRmodel)
                    elif ValidGeminiCommand(text):
                        command = text
                        FindGeminiCommand(command,db)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))


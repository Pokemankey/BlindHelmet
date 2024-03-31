from vosk import Model, KaldiRecognizer
import pyaudio
import json
#Module Imports
from Modules.VoiceBox.VoiceBoxSetup import getVoiceBox
from Modules.Config.config import SpeechRecognitionModelPath,MicrophoneIndex
from Modules.Detection.OCR.OCR_Setup import OCR_Setup
from Modules.Detection.ObjectDetection.ObjectDetection import ObjectDetection

from Modules.GarbageCollector.GarbageCollector import clean_pycache
from Modules.Config.Commands import ValidCommand,MatchCommand

def Jarvis():
    #Jarvis microphone setup
    model = Model(SpeechRecognitionModelPath)
    recognizer = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    device_index = MicrophoneIndex 
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000,
                    input_device_index=device_index)

    #Voice Module Setup
    engine = getVoiceBox()
    engine.say("jarvis online")
    engine.runAndWait()

    while True:
        data = stream.read(8000)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            resultMap = json.loads(result.lower())
            if ValidCommand(resultMap["text"]):
                print("Recognized:", result)
                if MatchCommand(resultMap["text"]) == "OCR":
                    print("ODC")
                    # OCR_Setup()
                elif MatchCommand(resultMap["text"]) == "ObjectDetection":
                    print("Object Detections")
                    # ObjectDetection()

    clean_pycache()

from vosk import Model, KaldiRecognizer
import pyaudio
import json
#Module Imports
from Modules.Config.config import AiName
from Modules.VoiceBox.VoiceBoxSetup import getVoiceBox
from Modules.Config.config import SpeechRecognitionModelPath,MicrophoneIndex
from Modules.Detection.OCR.OCR_Setup import OCR_Setup
from Modules.Detection.ObjectDetection.ObjectDetection import ObjectDetection
from Modules.Detection.HumanDetection.HumanDetection import HumanDetection
from Modules.Camera.CameraSetup import getCamera

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

    #Jarvis Camer Setup
    cap = getCamera()

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
                print("Recognized:", result)
                output = MatchCommand(resultMap["text"])
                if output == "OCR":
                    OCR_Setup(cap)
                elif output == "ObjectDetection":
                    ObjectDetection(cap)
                elif MatchCommand(resultMap["text"]) == "HumanDetection":
                    HumanDetection(cap)

    clean_pycache()

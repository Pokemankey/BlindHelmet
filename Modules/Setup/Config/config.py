# Path
TesseractPath = "/usr/bin/tesseract"
CocoModelPath = r"detection.pt"
faceRecognitionPath = r'Modules/Setup/Utility/haarcascade_frontalface_default.xml'
faceDatabasePath = r'Modules/Functions/Detection/FaceDetection/FaceDatabase'

# AI Settings
AiName = "zero"
DetectionConfidence = 0.7

# Camera Settings
CameraIndex = 0

# Microphone Settings
MicrophoneIndex = 4

# User Location
UserLocation = "Dubai,UAE"

# All Commands
# allCommands = "Ask Gemini A Question , OCR / Text Detection , Human Detection , Object Detection , Get weather information , Play youtube video / music and resume pause and stop the videos and lastly Get current date and time"
allCommands = "..."


# Enumerate available audio devices
import pyaudio
p = pyaudio.PyAudio()
print("Available audio devices:")
for i in range(p.get_device_count()):
   info = p.get_device_info_by_index(i)
   print(f"{i}: {info['name']}")

   

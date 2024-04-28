# Path
SpeechRecognitionModelPath = "/home/poke/BlindHelmet/Modules/Setup/Utility/Speech Recognition Model"
TesseractPath = "/bin/tesseract"
CocoModelPath = r"detection.pt"
faceRecognitionPath = r'Modules/Setup/Utility/haarcascade_frontalface_default.xml'
faceDatabasePath = r'Modules/Functions/Detection/FaceDetection/FaceDatabase'

# AI Settings
AiName = "zero"
DetectionConfidence = 0.7

# Camera Settings
CameraIndex = 0

# Microphone Settings
MicrophoneIndex = 1

# User Location
UserLocation = "Dubai,UAE"

# All Commands
# allCommands = "Ask Gemini A Question , OCR / Text Detection , Human Detection , Object Detection , Get weather information , Play youtube video / music and resume pause and stop the videos and lastly Get current date and time"
allCommands = "..."


# Enumerate available audio devices
import pyaudio
import cv2
p = pyaudio.PyAudio()
print("Available audio devices:")
for i in range(p.get_device_count()):
   info = p.get_device_info_by_index(i)
   print(f"{i}: {info['name']}")
camera_index = 0
while True:
    # Try to capture from the camera device
    cap = cv2.VideoCapture(camera_index)     
    # Check if the camera is opened successfully
    if not cap.isOpened():
        break    
    # Get the camera's name
    camera_name = f"Camera {camera_index}"      
    # Print camera information
    print(f"{camera_name}: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}x{cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")     
    # Release the capture object
    cap.release()
    # Move to the next camera device
    camera_index += 1

   

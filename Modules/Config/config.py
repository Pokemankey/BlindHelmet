# Path
SpeechRecognitionModelPath = r"C:\Users\moham\Desktop\MAJOR PROJECT\ClapTrap\Modules\Utility\Speech Recognition Model"
TesseractPath = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
CocoModelPath = r"C:\Users\moham\Desktop\MAJOR PROJECT\ClapTrap\Modules\Utility\detection.pt"


# AI Settings
AiName = "jarvis"
MatchPercentage = 70
DetectionConfidence = 0.7

# Camera Settings
CameraIndex = 1

# Microphone Settings
MicrophoneIndex = 0




# Enumerate available audio devices
# import pyaudio
# p = pyaudio.PyAudio()
# print("Available audio devices:")
# for i in range(p.get_device_count()):
#   info = p.get_device_info_by_index(i)
#   print(f"{i}: {info['name']}")
# Path
SpeechRecognitionModelPath = r"Modules\Setup\Utility\Speech Recognition Model"
TesseractPath = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
CocoModelPath = r"detection.pt"
NLPpath = r'C:\Users\moham\Desktop\MAJOR PROJECT\Blind Helmet\BlindHelmet-main\Modules\Setup\Utility\TrainInput\Zero-NLP.joblib'
tfidfPath = r'C:\Users\moham\Desktop\MAJOR PROJECT\Blind Helmet\BlindHelmet-main\Modules\Setup\Utility\TrainInput\Zero-tfidf_vectorizer.joblib'

# AI Settings
AiName = "Zero"
MatchPercentage = 70
DetectionConfidence = 0.7

# Camera Settings
CameraIndex = 0

# Microphone Settings
MicrophoneIndex = 1

# User Location
UserLocation = "Dubai,UAE"


# Enumerate available audio devices
# import pyaudio
# p = pyaudio.PyAudio()
# print("Available audio devices:")
# for i in range(p.get_device_count()):
#   info = p.get_device_info_by_index(i)
#   print(f"{i}: {info['name']}")
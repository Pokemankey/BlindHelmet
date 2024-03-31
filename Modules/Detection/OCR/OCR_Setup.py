import cv2
import pytesseract
#Module Imports
from Modules.VoiceBox.VoiceBoxSetup import getVoiceBox
from Modules.Camera.CameraSetup import getCamera
from Modules.Config.config import TesseractPath

def OCR_Setup():
    pytesseract.pytesseract.tesseract_cmd = TesseractPath
    engine = getVoiceBox()

    cap = getCamera()
    
    # Check if the camera is opened successfully
    if not cap.isOpened():
        engine.say("Error Failed to open camera.")
        engine.runAndWait()
        return

    ret, frame = cap.read()
    
    # Check if the frame is valid
    if not ret or frame is None:
        engine.say("Error Failed to capture frame from the camera.")
        engine.runAndWait()
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
    # Apply preprocessing techniques (e.g., denoising, binarization, deskewing)
    # Example:
    # gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    
    # Use Tesseract OCR to extract text from the document
    text = pytesseract.image_to_string(gray, config='--psm 6', lang='eng')
    engine.say(text)
    engine.runAndWait()

    cap.release()


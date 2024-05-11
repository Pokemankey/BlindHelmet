from doctr.io import DocumentFile
import cv2
import os

# Module Imports
from Modules.Setup.VoiceBox.VoiceBoxSetup import getVoiceBox
from Modules.Setup.Camera.CameraSetup import getCamera

def OCR_Setup(model):
    try:
        engine = getVoiceBox()

        cap = getCamera()
        # Check if the camera is opened successfully
        if not cap.isOpened():
            engine.say("Error Failed to open camera.")
            engine.runAndWait()
            return

        ret, frame = cap.read()
        cap.release()
        
        # Check if the frame is valid
        if not ret or frame is None:
            engine.say("Error Failed to capture frame from the camera.")
            engine.runAndWait()
            return

        # Save the frame as a temporary image file
        temp_image_path = "temp.png"
        cv2.imwrite(temp_image_path, frame)

        # Perform OCR on the temporary image
        doc = DocumentFile.from_images(temp_image_path)
        result = model(doc)
        json_output = result.export()

        sentence = ""
        for page in json_output["pages"]:
            for block in page["blocks"]:
                for line in block["lines"]:
                    for word in line["words"]:
                        sentence += word["value"] + " "

        # Speak the detected sentence
        print(sentence)
        engine.say(sentence)
        engine.runAndWait()

        # Delete the temporary image file
        os.remove(temp_image_path)
    except Exception as e:
        print("Error:", e)




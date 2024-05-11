#Module Imports
from Modules.Setup.VoiceBox.VoiceBoxSetup import speak
from Modules.Setup.Camera.CameraSetup import getCamera
from Modules.Setup.Config.config import CocoModelPath,DetectionConfidence

def ObjectDetection(detectionModel):
    names = detectionModel.names

    cap = getCamera()
    ret, frame = cap.read()
    cap.release()
    results = detectionModel.predict(frame, save=False, conf=DetectionConfidence)

    for r in results:
        obj = {}
        for c in r.boxes.cls:
            if(names[int(c)] not in obj):
                obj[names[int(c)]] = 1
                print(names[int(c)])
            else:
                obj[names[int(c)]] += 1
        for x in obj:
            speak(f"{obj[x]} {x}")
            
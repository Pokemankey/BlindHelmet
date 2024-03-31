from ultralytics import YOLO
#Module Imports
from Modules.VoiceBox.VoiceBoxSetup import getVoiceBox
from Modules.Camera.CameraSetup import getCamera
from Modules.Config.config import CocoModelPath,DetectionConfidence

def ObjectDetection():
    model = YOLO(CocoModelPath)
    engine = getVoiceBox()
    cap = getCamera()
    names = model.names

    ret, frame = cap.read()
    results = model.predict(frame, save=False, conf=DetectionConfidence)

    for r in results:
        obj = {}
        for c in r.boxes.cls:
            if(names[int(c)] not in obj):
                obj[names[int(c)]] = 1
                print(names[int(c)])
            else:
                obj[names[int(c)]] += 1
        for x in obj:
            engine.say(f"{obj[x]} {x}")
            engine.runAndWait()

    cap.release()
    engine.stop()

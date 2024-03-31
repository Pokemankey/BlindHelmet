from ultralytics import YOLO
#Module Imports
from Modules.Setup.VoiceBox.VoiceBoxSetup import getVoiceBox
from Modules.Setup.Config.config import CocoModelPath,DetectionConfidence

def HumanDetection(cap):
    model = YOLO(CocoModelPath)
    engine = getVoiceBox()
    names = model.names

    ret, frame = cap.read()
    results = model.predict(frame, save=False, conf=DetectionConfidence, classes = [0])

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

    engine.stop()
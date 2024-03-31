import cv2
from Modules.Setup.Config.config import CameraIndex

def getCamera():
    cap = cv2.VideoCapture(CameraIndex)
    return cap
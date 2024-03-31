import cv2
from Modules.Config.config import CameraIndex

def getCamera():
    cap = cv2.VideoCapture(CameraIndex)
    return cap
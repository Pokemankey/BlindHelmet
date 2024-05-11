import json
import cv2
import numpy as np
from imgbeddings import imgbeddings
from PIL import Image
import os
from scipy.spatial.distance import cosine

# Module Imports
from Modules.Setup.Config.config import faceRecognitionPath,faceDatabasePath
from Modules.Setup.Camera.CameraSetup import getCamera
from Modules.Setup.VoiceBox.VoiceBoxSetup import speak
from Modules.Setup.Microphone.Mic import getUserInput

def saveFace():
    cap = getCamera()
    try:
        ret, frame = cap.read()
        cap.release()
        haar_cascade = cv2.CascadeClassifier(faceRecognitionPath)
        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = haar_cascade.detectMultiScale(
            gray_img, scaleFactor=1.05, minNeighbors=1, minSize=(100, 100)
        )
        speak("What Is The Name Of This Person")
        
        name = getUserInput()
        isSaved = False
        for x, y, w, h in faces:
            cropped_image = gray_img[y:y + h, x:x + w]
            cropped_image = cv2.resize(cropped_image, (150, 150))
            target_file_name = 'Modules/Functions/Detection/FaceDetection/FaceDatabase/' + name + '.jpg'
            cv2.imwrite(target_file_name, cropped_image)
            print(name)
            speak(f"Saved Face Of {name}")
            
            isSaved = True
            break
        if not isSaved:
            speak(f"Could not find any person infront of the camera")
            
    except Exception as e:
        speak(f"Error Saving Image")
        

def precompute_embeddings():
    embeddings_dict = {}
    for file in os.listdir(faceDatabasePath):
        name = os.path.splitext(file)[0]
        embedding = get_embedding(os.path.join(faceDatabasePath, file))
        embeddings_dict[name] = embedding
    return embeddings_dict

def get_embedding(path):
    img = Image.open(path)
    ibed = imgbeddings()
    return ibed.to_embeddings(img)

def compare_embeddings(embedding1, embedding2):

    embedding1 = np.array(embedding1).flatten()
    embedding2 = np.array(embedding2).flatten()
    similarity_score = 1 - cosine(embedding1, embedding2)
    threshold = 0.7
    return similarity_score >= threshold

def saveTempFace(cap):
    try:
        ret, frame = cap.read()
        haar_cascade = cv2.CascadeClassifier(faceRecognitionPath)
        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = haar_cascade.detectMultiScale(
            gray_img, scaleFactor=1.05, minNeighbors=1, minSize=(100, 100)
        )
        for x, y, w, h in faces:
            cropped_image = frame[y:y + h, x:x + w]
            target_file_name = 'Modules/Functions/Detection/FaceDetection/Face/' + 'temp' + '.jpg'
            cv2.imwrite(target_file_name, cropped_image)
    except Exception as e:
        print("Error saving temp face")

def detectFace(known_faces):
    cap = getCamera()
    try:
        saveTempFace(cap)
        # Compare the embeddings of the detected face with precomputed embeddings
        for file in os.listdir('Modules/Functions/Detection/FaceDetection/Face'):
            embedding = get_embedding(os.path.join('Modules/Functions/Detection/FaceDetection/Face', file))
            isFound = False
            for known_name, known_embedding in known_faces.items():
                if compare_embeddings(embedding, known_embedding):
                    print(f"Detected {known_name}")
                    speak(f"Detected {known_name}")
                    
                    isFound = True
        temp_file_path = 'Modules/Functions/Detection/FaceDetection/Face/temp.jpg'
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        cap.release()
        if not isFound:
            speak(f"COuld Not Find Anyone")
            
    except Exception as e:
        print(e)
        speak("Error Recognizing Face")
        

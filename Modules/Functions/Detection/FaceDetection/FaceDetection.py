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
from Modules.Setup.VoiceBox.VoiceBoxSetup import getVoiceBox

def saveFace(recognizer,stream):
    engine = getVoiceBox()
    engine.say("What Is The Name Of This Person")
    engine.runAndWait()
    cap = getCamera()
    try:
        ret, frame = cap.read()
        cap.release()
        name = ""
        while True:
            data = stream.read(2000)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                resultMap = json.loads(result.lower())
                print(resultMap['text'])
                name = resultMap['text']
                break

        haar_cascade = cv2.CascadeClassifier(faceRecognitionPath)
        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = haar_cascade.detectMultiScale(
            gray_img, scaleFactor=1.05, minNeighbors=1, minSize=(100, 100)
        )

        for x, y, w, h in faces:
            cropped_image = gray_img[y:y + h, x:x + w]
            cropped_image = cv2.resize(cropped_image, (150, 150))
            target_file_name = 'Modules\\Functions\\Detection\\FaceDetection\\FaceDatabase\\' + name + '.jpg'
            cv2.imwrite(target_file_name, cropped_image)

        engine.say(f"Saved Face Of {name}")
        engine.runAndWait()
    except Exception as e:
        engine.say(f"Error Saving Image")
        engine.runAndWait()

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
    threshold = 0.9
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
            target_file_name = 'Modules\\Functions\\Detection\\FaceDetection\\Face\\' + 'temp' + '.jpg'
            cv2.imwrite(target_file_name, cropped_image)
    except Exception as e:
        print("Error saving temp face")

def detectFace(known_faces):
    engine = getVoiceBox()
    cap = getCamera()
    try:
        saveTempFace(cap)
        # Compare the embeddings of the detected face with precomputed embeddings
        for file in os.listdir('Modules\\Functions\\Detection\\FaceDetection\\Face'):
            embedding = get_embedding(os.path.join('Modules\\Functions\\Detection\\FaceDetection\\Face', file))
            for known_name, known_embedding in known_faces.items():
                if compare_embeddings(embedding, known_embedding):
                    print(f"Detected {known_name}")
                    engine.say(f"Detected {known_name}")
                    engine.runAndWait()
        temp_file_path = 'Modules\\Functions\\Detection\\FaceDetection\\Face\\temp.jpg'
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        cap.release()
        
    except Exception as e:
        print(e)
        engine.say("Error Recognizing Face")
        engine.runAndWait()

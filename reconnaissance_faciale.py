import pickle
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('C:/Users/EG/anaconda3/Lib/site-packages/cv2/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer.create()
recognizer.read('trainner.yml')
id_image = 0
#color_info = (255,255,255)
color_know = (0,255,0)
color_unknow = (0,0,255)

with open('labels.pickle', "rb") as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4, minSize=(50,50))
    if ret == True:
        for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (50, 50))
            id_, conf= recognizer.predict(roi_gray)
            if conf <= 115:
                color = color_know
                name = labels[id_]
            else:
                color = color_unknow
                name = "inconnu"
            label = f"{name} {conf}f"
            cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_DUPLEX, 1, color, 1, cv2.LINE_AA)
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
        cv2.imshow('Begin_looking',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
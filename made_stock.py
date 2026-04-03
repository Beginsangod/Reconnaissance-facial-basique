import cv2
import os
import sys

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('C:/Users/EG/anaconda3/Lib/site-packages/cv2/data/haarcascade_frontalface_alt2.xml')
save_face = False
repertoire = sys.argv[1]
sujet = sys.argv[1]
n = 0

while (cap.isOpened()):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4, minSize=(50,50))

    if ret == True:
        for (x,y,w,h) in faces:
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (50, 50))
            if save_face == True:
                name_file = f"data_image/{repertoire}/{sujet}{n}.png"
                if not os.path.isdir(f"data_image/{repertoire}"):
                    os.makedirs(f"data_image/{repertoire}")
                cv2.imwrite(name_file, roi_gray)
                n += 1
                print("write ", n)
        cv2.imshow('Begin_looking',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif cv2.waitKey(1) & 0xFF == ord('s'):
            save_face = not save_face
            print(save_face)

cap.release()
cv2.destroyAllWindows()
import cv2
import numpy as np  
import os 
import pickle

data_dir = "data_image"
current_id = 0
label_ids = {}
x_train = []
y_label = []

for root, dirs, files in os.walk(data_dir):
    if len(files):
        label = root.split("\\")[-1]
        for file in files:
            path= os.path.join(root, file)
            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1
            id_ = label_ids[label]
            image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            x_train.append(image)
            y_label.append(id_)

with open("labels.pickle", "wb") as f:
    pickle.dump(label_ids, f)

x_train = np.array(x_train)
y_label = np.array(y_label)
recognizer = cv2.face.LBPHFaceRecognizer.create()
recognizer.train(x_train, y_label)
recognizer.save("trainner.yml")


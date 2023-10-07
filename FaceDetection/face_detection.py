import numpy
import cv2
import os

directory = '\\'.join(__file__.split('\\')[:-1])

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
fake_smile = cv2.imread(directory+"\\assets\\peksmel.png", cv2.IMREAD_UNCHANGED)

while True:
    detected_face = 0
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 3, minSize=(120, 120))
    
    for (x, y, w, h) in faces:
        print(x, y, w, h)
        fake_smile_copy = numpy.copy(fake_smile)
        fake_smile_copy = cv2.resize(fake_smile_copy, (w, h))
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 6)
        if y > 50 and x > 50 and (y+h) < len(frame) and (x+w) < len(frame[0]):
            frame[(y-50):(y+h+50)][(x-50):(x+w+50)] = fake_smile_copy
        elif y > 50 and x > 50:
            frame[(y-50):(y+h)][(x-50):(x+w)] = fake_smile_copy
        elif (y+h) < len(frame) and (x+w) < len(frame[0]):
            frame[(y):(y+h+50)][(x):(x+w+50)] = fake_smile_copy
        else:
            frame[(y):(y+h)][(x):(x+w)] = fake_smile_copy

        # frame[y:(y+h)] 
        detected_face+=1
    
    frame = cv2.flip(frame, 1)
    cv2.putText(frame, f"Detected Face : {detected_face}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("Face Detection", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


import numpy as np
import cv2
import imageProcessing as imgprocess

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    img = imgprocess.rec(frame)
    cv2.imshow('Screen', img)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
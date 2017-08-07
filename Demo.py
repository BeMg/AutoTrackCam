import cv2
from GetVideoFromCam import GetVideoFromCam
from utils import draw
from DetectPeople import DetectPeople
from HOG import HOGdetect


cap = GetVideoFromCam(0)

while True:
    flag, frame = cap.read()
    
    
    cv2.imshow('GGG', frame)
    if cv2.waitKey(5) == 27:
        cap.release()
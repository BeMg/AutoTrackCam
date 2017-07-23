import cv2
from GetVideoFromCam import GetVideoFromCam
from utils import draw, DetectFace
from DetectBody import DetectBody
import imutils
 

cap = GetVideoFromCam(0)

while True:
    flag, frame = cap.read()

    rects = DetectFace(frame)

    if len(rects) > 0:
        draw(frame, rects, (255, 0, 0))
    
    cv2.imshow('GGG', frame)
    if cv2.waitKey(5) == 27:
        cap.release()
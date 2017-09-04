import cv2
from GetVideoFromCam import GetVideoFromCam
from utils import draw
from DetectPeople import DetectPeople
from DetectScreen import DetectScreen

cap = GetVideoFromCam(0)

while True:
    flag, frame = cap.read()
    People_rects = DetectPeople(frame)

    if len(People_rects) > 0:
        draw(frame, People_rects, (255, 0, 0))

    cv2.imshow('Frame', frame)
    if cv2.waitKey(5) == 27:
        cap.release()

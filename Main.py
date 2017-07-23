import cv2
from GetVideoFromCam import GetVideoFromCam
from utils import draw
from DetectBody import DetectBody
import imutils
 

cap = GetVideoFromCam('./media/2.mp4')

cnt = 0
while True:
    cnt = cnt + 1
    flag, frame = cap.read()

    frame = imutils.resize(frame , 480)

    if cnt%30 == 0:
        rects = DetectBody(frame)

        print(rects)

        if len(rects) > 0:
            draw(frame, rects, (255, 0, 0))
    
    cv2.imshow('GGG', frame)

    if cv2.waitKey(5) == 27:
        cap.release()
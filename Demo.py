import cv2
from GetVideoFromCam import GetVideoFromCam
from utils import draw2
from DetectUpperBody import DetectUpperBody
from DetectBody import DetectBody

cap = GetVideoFromCam(0)

while True:
    flag, frame = cap.read()

    print(frame.shape)    
    h, w, _ = frame.shape

    # frame = cv2.resize(frame, (int(w/5), int(h/5)))

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    rects = DetectUpperBody(gray)

    if len(rects) > 0:
        draw2(frame, rects, (255, 0, 0))

    cv2.imshow('GGG', frame)
    if cv2.waitKey(5) == 27:
        cap.release()
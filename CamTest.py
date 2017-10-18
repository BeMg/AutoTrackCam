import cv2
from DetectUpperBody import DetectUpperBody
from DetectBody import DetectBody
from utils import draw, DetectFace  


cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

while True:
    flag, frame = cap.read()

    rects = DetectFace(frame)

    draw(frame, rects, (0,255,0))

    out.write(frame)
    cv2.imshow('a', frame)

    if cv2.waitKey(5) == 27:
        cap.release()

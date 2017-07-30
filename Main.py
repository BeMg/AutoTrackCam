import cv2
from GetVideoFromCam import GetVideoFromCam
from utils import draw
from DetectPeople import DetectPeople
from DetectScreen import DetectScreen
 

cap = GetVideoFromCam(0)

'''
mode = 0
find the start position
mode = 1
chasing the follow position

after 20 frame mode 1 -> 0 
find people mode 0 -> 1
'''
mode = 0

while True:
    flag, frame = cap.read()

    if mode == 0:
        People_rects = DetectPeople(frame)
    else:
        # Wait to work
        # People_rects = kfilter(frame)

    Screen_rects = DetectScreen(frame)

    if len(rects) > 0:
        draw(frame, People_rects, (255, 0, 0))
    
    cv2.imshow('GGG', frame)
    if cv2.waitKey(5) == 27:
        cap.release()
import cv2

cap = cv2.VideoCapture('/home/hchusiang/AutoTrackCam/media/output.avi')

while True:
    _flag, frame = cap.read()
    cv2.imshow('Frame', frame)
    if cv2.waitKey(5) == 27:
        cap.release()
        break
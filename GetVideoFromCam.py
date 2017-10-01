import cv2

def GetVideoFromCam(VideoSource):
    cap = cv2.VideoCapture(VideoSource)
    print(cap.isOpened())
    return cap
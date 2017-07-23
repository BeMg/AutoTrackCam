from utils import DetectFace

def DetectPeople(frame):
    rects = DetectFace(frame)
    if len(rects) > 0:
        return rects
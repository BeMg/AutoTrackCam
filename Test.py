import cv2
import multiprocessing as mp
from GetVideoFromCam import GetVideoFromCam
from utils import draw
from DetectPeople import DetectPeople
from DetectScreen import DetectScreen
import Tracking
import Stepper
from Action import action


def capFrameProcess(cap, conn):
    while True:
        _flag, frame = cap.read()
        conn.send(frame)

def InitializeObj():
    track_container = Tracking.objTracking()

    return track_container

if __name__ == '__main__':


    # Creat a process for capturing frame
    cap = GetVideoFromCam(0)
    mp.set_start_method('fork')
    par_conn, child_conn = mp.Pipe()
    p = mp.Process(target=capFrameProcess, args=(cap, child_conn,))
    p.start()

    #Initialize object
    track_container = InitializeObj()

    # If reset, the whole system will start at detection
    reset = False

    while True:
        frame = par_conn.recv()
        People_rects = DetectPeople(frame)
        if len(People_rects) > 0:
            draw(frame, People_rects, (255, 0, 0))
            print(People_rects)
            track_container.setWindow(frame, People_rects)
        else:
            continue
        while True:
            frame = par_conn.recv()
            People_rects = track_container.getRect(frame)
            action(frame, People_rects)
            draw(frame, People_rects, (255, 0, 0))
            cv2.imshow('Frame', frame)
            if cv2.waitKey(5) == 27:
                p.join()
                cap.release()

        

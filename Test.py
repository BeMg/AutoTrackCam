import cv2
import multiprocessing as mp
from GetVideoFromCam import GetVideoFromCam
from utils import draw
from DetectPeople import DetectPeople
from DetectScreen_old import DetectScreen
import Tracking
from sshTrun import action
import paramiko
#import Stepper
#from Action import action


hostname = '10.0.0.100'
port = 22
username = 'pi'
password = 'raspberry'


def capFrameProcess(cap, conn):
    while True:
        _flag, frame = cap.read()
        conn.send(frame)

def InitializeObj():
    track_container = Tracking.objTracking()

    return track_container

if __name__ == '__main__':

    ## ssh connection
    paramiko.util.log_to_file('paramiko.log')
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.connect(hostname, port, username, password)

    # Creat a process for capturing frame
    cap = GetVideoFromCam(0)
    #cap = cv2.VideoCapture('/home/hchusiang/AutoTrackCam/media/output.avi')

    # If reset, the whole system will start at detection
    reset = True
    cnt = 0
    track_container = InitializeObj()
    while True:
        while reset is True:
            #Initialize object
            track_container = InitializeObj()
            #Read frame
            _flag, frame = cap.read()
            #Detect
            People_rects = DetectPeople(frame)
            if len(People_rects) > 0:
                track_container.setWindow(frame, People_rects)
                reset = False
            else:
                cv2.imshow('Frame', frame)

        #Tracking Stage
        while cnt < 50:
            cnt = cnt + 1
            if cnt >= 50:
                reset = True
                cnt = 0
                print("Reset")

            _flag, frame = cap.read()
            People_rects = track_container.getRect(frame)
            Screen_rects = DetectScreen(frame)
            draw(frame, People_rects, (255, 0, 0))
            draw(frame, Screen_rects, (0, 255, 0))
            action(frame, People_rects, s)
            cv2.imshow('Frame', frame)
            if cv2.waitKey(5) == 27:
                cap.release()
            

"""
    while True:
        track_container = InitializeObj()
        reset = False
        cnt = 0
        _flag, frame = cap.read()
        People_rects = DetectPeople(frame)
        if len(People_rects) > 0:
            draw(frame, People_rects, (255, 0, 0))
            print(People_rects)
            track_container.setWindow(frame, People_rects)
        else:
            cv2.imshow('Frame', frame)
            continue
        while reset is False:
            cnt = cnt + 1
            reset = True if cnt >= 50 else False
            cnt = 0 if reset is True else cnt + 1
            _flag, frame = cap.read()
            People_rects = track_container.getRect(frame)
            Screen_rects = DetectScreen(frame)
            #action(frame, People_rects)
            draw(frame, People_rects, (255, 0, 0))
            draw(frame, Screen_rects, (0, 255, 0))
            cv2.imshow('Frame', frame)
            if cv2.waitKey(5) == 27:
                cap.release()

        
"""
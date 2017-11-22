import cv2
import multiprocessing as mp
from GetVideoFromCam import GetVideoFromCam
from utils import draw, draw2
from DetectPeople import DetectPeople
from DetectUpperBody import DetectUpperBody
from DetectScreen_old import DetectScreen
import Tracking
from sshTrun import action
import paramiko
import time
#import Stepper
#from Action import action


hostname = '192.168.43.29'
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

    time.sleep(5)
    ## ssh connection
    paramiko.util.log_to_file('paramiko.log')
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.connect(hostname, port, username, password)

    # Creat a process for capturing frame
    cap = GetVideoFromCam(1)
    #cap = cv2.VideoCapture('/home/hchusiang/AutoTrackCam/media/output.avi')

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

    # If reset, the whole system will start at detection
    reset = True
    cnt = 0
    color = None
    track_container = InitializeObj()
    while True:
        while reset is True:
            #Initialize object
            track_container = None
            track_container = InitializeObj()
            #Read frame
            _flag, frame = cap.read()
            #Detect
            People_rects = DetectPeople(frame)
            UpperBody_rects = DetectUpperBody(frame)
            if len(People_rects) > 0:
                track_container.setWindow(frame, People_rects)
                color = (255, 0, 0)
                reset = False
            elif len(UpperBody_rects) > 0:
                col, row, width, length = UpperBody_rects[0]
                People_rects = UpperBody_rects
                track_container.setWindow(frame, People_rects)
                cv2.imwrite('upper.png', frame)
                color = (0, 255, 0)
                reset = False
            else:
                cv2.imshow('Frame', frame)
                out.write(frame)
                continue

        #Tracking Stage
        while cnt < 30:
            cnt = cnt + 1
            if cnt >= 30:
                reset = True
                cnt = 0
                break

            _flag, frame = cap.read()
            People_rects = track_container.getRect(frame)
            Screen_rects = DetectScreen(frame)
            draw(frame, People_rects, color)
            draw(frame, Screen_rects, (0, 0, 255))
            if action(frame, People_rects, s) is True:
                reset = True
                break
            out.write(frame)
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
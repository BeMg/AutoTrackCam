import cv2
import multiprocessing as mp
from GetVideoFromCam import GetVideoFromCam
from utils import draw, draw2
from DetectPeople import DetectPeople
from DetectUpperBody import DetectUpperBody
from DetectScreen_old import DetectScreen
import Tracking
from sshTrun import action, resetAction
import paramiko
import time
#import Stepper
#from Action import action


hostname = '192.168.43.29'
port = 22
username = 'pi'
password = 'raspberry'


def InitializeObj():
    track_container = Tracking.objTracking()

    return track_container

if __name__ == '__main__':

    time.sleep(5)
    ## ssh connection
    '''
    paramiko.util.log_to_file('paramiko.log')
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.connect(hostname, port, username, password)
    '''
    # Creat a process for capturing frame
    cap = GetVideoFromCam(1)
    #cap = cv2.VideoCapture('/home/hchusiang/AutoTrackCam/media/output.avi')

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

    # If reset, the whole system will start at detection
    reset = True
    cnt = 0
    cnt_turns = 0
    lost = 0
    color = None
    track_container = InitializeObj()

    while True:
        while reset is True:

            track_container = InitializeObj()
            _flag, frame = cap.read()

            People_rects = DetectPeople(frame)
            if len(People_rects) > 0:
                track_container.setWindow(frame, People_rects)
                color = (255, 0, 0)
                reset = False
            else:
                UpperBody_rects = DetectUpperBody(frame)
                if len(UpperBody_rects) > 0:
                    track_container.setWindow(frame, People_rects)
                    color(0, 255, 0)
                    reset = False
                else:
                    cv2.imshow('Frame', frame)
                    out.write(frame)
                    lost = lost + 1
                    if lost > 50:
                        resetAction(cnt_turns, s)
                        lost = 0
                    continue
            
        #Tracking Stage
        while cnt < 50:
            cnt = cnt + 1
            if cnt > 50:
                reset = True
                cnt = 0
                break

            _flag, frame = cap.read()
            People_rects = track_container.getRect(frame)
            draw(frame, People_rects, color)
            draw(frame, Screen_rects, (0, 0, 255))
            isAction ,cnt_turns = action(frame, People_rects, s, cnt_turns)
            if isAction is True:
                reset = True
                break
            out.write(frame)
            cv2.imshow('Frame', frame)
            if cv2.waitKey(5) == 27:
            cap.release()


import paramiko
import sys
hostname = '10.0.0.100'
port = 22
username = 'pi'
password = 'raspberry'




def action(img, rect, s):
    height, weight, _ignore = img.shape
    print(rect[0][0], rect[0][2])
    bonduary = (weight * 0.2, weight * 0.8)
    print(bonduary)

    center = int((rect[0][2] + rect[0][0]) / 2)

    if center < bonduary[0]:
        stdin, stdout, stderr = s.exec_command('python3 /home/pi/AutoTrackCam/remoteTurn.py 29 31 33 35 -5')
        return True
    if center > bonduary[1]:
        stdin, stdout, stderr = s.exec_command('python3 /home/pi/AutoTrackCam/remoteTurn.py 29 31 33 35 5')
        return True

    return False

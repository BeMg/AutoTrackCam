import RPi.GPIO as GPIO
import time
import sys
from array import *

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)

clockwise = 1
steps = 180

ports = [29,31,33,35]
for p in ports:
    GPIO.setup(p,GPIO.OUT)

def TurnCam(steps,clockwise):
    arr = [[0,1,2,3],[3,2,1,0]]
    for x in range(0,steps):
        for j in arr[clockwise]:
            time.sleep(0.01)
            for i in range(0,4):
                if i == j:            
                    GPIO.output(ports[i],True)
                else:
                    GPIO.output(ports[i],False)




import Stepper
import numpy as np
import cv2
import time
import RPi.GPIO as GPIO
def action(img, rect):

    height, weight, _ignore = img.shape
    print(rect[0][0], rect[0][2])
    bonduary = (weight * 0.2, weight * 0.8)
    print(bonduary)
    GPIO.setmode(GPIO.BOARD)
    motor = Stepper.Motor((29, 31, 33, 35), 15)

    center = int((rect[0][2] + rect[0][0]) / 2)

    if center < bonduary[0]:
        print("Here")
        #motor.move_to(0)
        motor.move_to(-5) #counterclockwise
        time.sleep(0.15)
        return True
        GPIO.cleanup()
    
    if center > bonduary[1]:
        print("Here2")
        #motor.move_to(0)
        motor.move_to(5) #clockwise
        time.sleep(0.15)
        return True
        GPIO.cleanup()

    GPIO.cleanup()
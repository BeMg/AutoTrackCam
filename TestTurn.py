#!/usr/bin/python

from Stepper import Motor
from time import sleep
import RPi.GPIO as GPIO
import sys
from TurnCam import TurnCam

if __name__ == "__main__":
	GPIO.setmode(GPIO.BOARD)

	m = Motor([int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])], 15)

	# clock 180
	m.move_to(5)
	GPIO.cleanup()
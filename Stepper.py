#!/usr/bin/env python

# Class to control the 28BJY-48 stepper motor with ULN2003 control board.
# Converted from work done by Stephen Phillips (www.scphillips.com)

from time import sleep
import RPi.GPIO as GPIO
 
class Motor:
    def __init__(self, revs_per_minute):
        for p in pins:
            GPIO.setup(p, GPIO.OUT)
            GPIO.output(p, 0)

        self.P1 = 29
        self.P2 = 31
        self.P3 = 33
        self.P4 = 35

        self.deg_per_step = 5.625 / 64
        self.steps_per_rev = int(360 / self.deg_per_step)  # 4096
        self.step_angle = 0  # Assume the way it is pointing is zero degrees
        self._rpm = revs_per_minute

        # T is the amount of time to stop between signals
        self._T = (60.0 / self._rpm) / self.steps_per_rev
 
    def move_to(self, angle):
        """Take the shortest route to a particular angle (degrees)."""
        # Make sure there is a 1:1 mapping between angle and stepper angle
        target_step_angle = 8 * (int(angle / self.deg_per_step) / 8)
        steps = target_step_angle - self.step_angle
        steps = int(steps % self.steps_per_rev)
        if steps > self.steps_per_rev / 2:
            steps -= int(self.steps_per_rev)
            print("moving " + str(steps) + " steps")
            self._move_acw(-steps / 8)
        else:
            print("moving " + str(steps) + " steps")
            self._move_cw(steps / 8)
        self.step_angle = target_step_angle

    def move_acw(self, angle):
        target_step_angle = (int(angle / self.deg_per_step) / 8)
        steps = target_step_angle
        steps = int(steps % self.steps_per_rev)
        self._move_acw(steps)
        self.step_angle = self.step_angle - angle
 
    def _move_cw(self, big_steps):
        GPIO.output(self.P1, 0)
        GPIO.output(self.P2, 0)
        GPIO.output(self.P3, 0)
        GPIO.output(self.P4, 0)

        big_steps = int(big_steps)

        for i in range(big_steps):
            GPIO.output(self.P4, 1)
            sleep(self._T)
            GPIO.output(self.P2, 0)
            sleep(self._T)
            GPIO.output(self.P3, 1)
            sleep(self._T)
            GPIO.output(self.P1, 0)
            sleep(self._T)
            GPIO.output(self.P2, 1)
            sleep(self._T)
            GPIO.output(self.P4, 0)
            sleep(self._T)
            GPIO.output(self.P1, 1)
            sleep(self._T)
            GPIO.output(self.P3, 0)
            sleep(self._T)
 
    def _move_acw(self, big_steps):
        GPIO.output(self.P1, 0)
        GPIO.output(self.P2, 0)
        GPIO.output(self.P3, 0)
        GPIO.output(self.P4, 0)

        big_steps = int(big_steps)

        for i in range(big_steps):
            GPIO.output(self.P3, 0)
            sleep(self._T)
            GPIO.output(self.P1, 1)
            sleep(self._T)
            GPIO.output(self.P4, 0)
            sleep(self._T)
            GPIO.output(self.P2, 1)
            sleep(self._T)
            GPIO.output(self.P1, 0)
            sleep(self._T)
            GPIO.output(self.P3, 1)
            sleep(self._T)
            GPIO.output(self.P2, 0)
            sleep(self._T)
            GPIO.output(self.P4, 1)
            sleep(self._T)

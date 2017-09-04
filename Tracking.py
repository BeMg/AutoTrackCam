import cv2
import numpy as np
import CamShift as cs

class objTracking(object):
    
    def __init__(self, rect):
        self.rect = rect
        self.window = None
        self.roiHist = None
        self.center = None
        self.width, self.length = cs.setWindowSize(self.rect)
    
    def setWindow(img, rect):
        self.window, self.roiHist = cs.setWindow(img, rect)
    
    def getRect(img):

        self.window, self.center, _pts = cs.camShift(img, self.window, self.roiHist)
        
        x1 = if self.center[0] - (self.length / 2) > 0: self.center[0] - (self.length / 2) else 0
        y1 = if self.center[1] - (self.width / 2) > 0: self.center[1] - (self.width / 2) else 0

        col, row, _ignore = img.shape
        x2 = if self.center[0] + (self.length / 2) < col: self.center[0] + (self.length / 2) else col
        y2 = if self.center[1] + (self.width / 2) < row: self.center[1] + (self.width / 2) else row

        return ((x1, y1), (x2, y2))


import cv2
import numpy as np
import CamShift as cs

class objTracking(object):
    
    def __init__(self):
        self.rect = None
        self.window = None
        self.roiHist = None
        self.center = None
        self.width = None
        self.length = None
    
    def setWindow(self, img, rect):
        self.window, self.roiHist = cs.setWindow(img, rect)
        self.width, self.length = cs.setWindowSize(rect)
    
    def getRect(self, img):

        self.window, self.center, _pts = cs.camShift(img, self.window, self.roiHist)
        
        #x1 = if self.center[0] - (self.length / 2) > 0: self.center[0] - (self.length / 2) else 0
        x1 =  self.center[0] - (self.length / 2) if self.center[0] - (self.length / 2) > 0 else 0
        #y1 = if self.center[1] - (self.width / 2) > 0: self.center[1] - (self.width / 2) else 0
        y1 = self.center[1] - (self.width / 2)  if self.center[1] - (self.width / 2) > 0 else 0

        row, col, _ignore = img.shape
        #x2 = if self.center[0] + (self.length / 2) < col: self.center[0] + (self.length / 2) else col
        x2 = self.center[0] + (self.length / 2) if self.center[0] + (self.length / 2) < col else col
        #y2 = if self.center[1] + (self.width / 2) < row: self.center[1] + (self.width / 2) else row
        y2 = self.center[1] + (self.width / 2)  if self.center[1] + (self.width / 2) < row else row

        return [[int(x1), int(y1), int(x2), int(y2)]]


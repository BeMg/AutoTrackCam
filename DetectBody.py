from __future__ import print_function
import cv2
import numpy as np

def DetectBody(frame):

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    (rects, weight) = hog.detectMultiScale(frame)
    
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    # pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    return rects
    
import cv2
import numpy as np
from detectanddraw import draw
from TurningWithDetect import Turn


def calculateRect(contour, size):

    contour = contour[np.argsort(contour[:, 0])]
    contour = contour[np.argsort(contour[:, 1])]

    leftTop = contour[0]
    rightDown = contour[len(contour)]

    rect = [leftTop, rightDown]

    return rect
    

def selectScreen(contours):

    area = -1.0
    result = contours[0]

    for contour in contours:
        curr = cv2.contourArea(contour)
        if curr > area:
            curr = area
            result = contour

        return result



def DetectScreen(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 21)
    ret, binarythresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY +cv2.THRESH_OTSU)

    img2, contours, hierarchy = cv2.findContours(binarythresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if hierarchy is None:
        return [] 

    rect = selectScreen(contours)

    return rect
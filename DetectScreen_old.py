import cv2
import numpy as np
from detectanddraw import draw
from TurningWithDetect import Turn

def PolygonArea(corners):
    #n = len(corners) # of corners
    #print(corners)
    #print(corners.shape)
    l, m, n = corners.shape
    area = 0.0
    for i in range(l):
        j = (i + 1) % l
        area += corners[i][0][0] * corners[j][0][1]
        area -= corners[j][0][0] * corners[i][0][1]
    area = abs(area) / 2.0
    return area

def selectScreen(contours):
    x = np.array([[1, 2]])
    toReturn = contours[0]
    left = np.array([[]])
    right = np.array([[]])
    maxArea = -1.0
    for c in contours:
        area = PolygonArea(c)
        if(area > maxArea):
            maxArea = area
            toReturn = c
    #print(np.array_repr(toReturn).replace('\n', ''))
    l, m, n = toReturn.shape
    toReturn = toReturn.reshape(l, n)
    #print(np.array_repr(toReturn).replace('\n', ''))
    lx = 640
    ly = 480
    rx = -1
    ry = -1
    for i in toReturn:
        if(i[0] < lx): lx = i[0]
        if(i[1] < ly): ly = i[1]
        if(i[0] > rx): rx = i[0]
        if(i[1] > ry): ry = i[1]

    return c, [lx, ly], [rx, ry]

def screenState(left, right, length, height):
    stateBoundary = 0 # 0 for vaild, 1 for out of left boundary, 2 for out of right boundary
    stateVisible = 0 # 0 for vaild , 1 for out of visible
    leftBound = length * 0.1
    rightBound = length * 0.9
    if(left[0] < leftBound):
        print("Screen out of the left boundary")
       # Turn(2, 1) 
        stateBoundary = 1
    elif(right[0] > rightBound):
        print("Screen out of the right boundary")
       # Turn(2, 0)
        stateBoundary = 2
    if( (right[0] - left[0]) * (right[1] - left[1]) < length * height * 0.4):
        print("Screen isn't visvible, Do the operation")
        stateVisible = 1
    if(stateBoundary == 0 and stateVisible == 0):
        print("Maintain the state")
    return [stateBoundary, stateVisible]


def DetectScreen(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 21)
    ret, binarythresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY +cv2.THRESH_OTSU)

    img2, contours, hierarchy = cv2.findContours(binarythresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    coordLeft = []
    coordRight = []

    if hierarchy is None:
        return [] 

    screen, coordLeft, coordRight = selectScreen(contours)

    result = list()
    result.append(coordLeft[0])
    result.append(coordLeft[1])
    result.append(coordRight[0])
    result.append(coordRight[1])

    return result
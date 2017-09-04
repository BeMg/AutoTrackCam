import cv2
import numpy as np

termCrit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

def setWindowSize(rect):
    width = rect[0][3] - rect[0][1]
    length = rect[0][2] - rect[0][0]

    return width, length

def setWindow(img, rect):
    
    col, row, width, length = rect[0]
    cv2.imwrite('init.png', img[row: length, col: width])
    window = (col, row, width, length)
    roi = img[row : length, col : width]
    hsvRoi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsvRoi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
    roiHist = cv2.calcHist([hsvRoi],[0],mask,[180],[0,180])
    cv2.normalize(roiHist,roiHist,0, 255, cv2.NORM_MINMAX)

    return window, roiHist


def camShift(img, window, roiHist):
    
    #window, roiHist = setWindow(img, rect)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0], roiHist, [0, 180], 1)

    rect, window = cv2.CamShift(dst, window, termCrit)
    #print(window)
    pts = cv2.boxPoints(rect)
    pts = np.int0(pts)
    #print(pts)
    #img2 = cv2.polylines(img,[pts],True, 255,2)
    center = np.mean(pts, axis = 0)
    center = np.int0(center)
    
    return window, center, pts

def getForeground(img, rect):

    mask = np.zeros(img.shape[:2],np.uint8)

    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)

    cv2.grabCut(img,mask,rect,bgdModel,fgdModel,3,cv2.GC_INIT_WITH_RECT)

    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    toReturn = img*mask2[:,:,np.newaxis]

    return toReturn
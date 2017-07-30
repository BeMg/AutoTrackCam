import cv2
import numpy as np

termCrit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

def setWindow(img, rects):
    
    """
        Initial tracking window for camshift,
        depending on argument rects and Historgram of ROI

        Args:
            img: Current frame
            rects: Coordinate of the tracking setWindow
        
        Return:
            window: (Tuple) Coordinate of the tracking setWindow
            roiHist: Historgram of ROI

    """

    # col, row, width, length = rects[0]
    # window = (col, row, width, length)
    x1, y1, x2, y2 = rects[0]
    window = (x1, y1, x2 - x1, y2 - y1)
    
    roi = img[y1 : y2, x1 : x2]
    hsvRoi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsvRoi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
    roiHist = cv2.calcHist([hsvRoi],[0],mask,[180],[0,180])
    cv2.normalize(roiHist,roiHist,0, 255, cv2.NORM_MINMAX)

    return window, roiHist

def camShift(img, window, roiHist):
    
    """
        Operates camshift

        Args:
            img: Current frame
            window: tracking window returned by setWindow()
            roiHist: Historgram of ROI returned by setWindow()
            
        Return:
            center: center of the mass of the object
            pts: Polygon by camshift()

    """
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0], roiHist, [0, 180], 1)

    rect, window = cv2.CamShift(dst, window, termCrit)
    
    pts = cv2.boxPoints(rect)
    pts = np.int0(pts)
    
    center = np.mean(pts, axis = 0)
    center = np.int0(center)
    
    return center, pts

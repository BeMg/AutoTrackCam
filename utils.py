import cv2
import numpy as np
from sklearn import svm


def detect(img, cascade):

    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(10, 10),
                                     flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    return rects


def draw(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

def draw2(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x1+x2, y1+y2), color, 2)

def face_cascade():
    cascade_xml = []

    cascade_xml.append('./haarcascades/haarcascade_frontalface_alt2.xml')

    cascades = []

    for i, xml in enumerate(cascade_xml):
        cascades.append(cv2.CascadeClassifier(xml))

    return cascades

def DetectFace(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascades = face_cascade()
    rects = detect(img, cascades[0])
    return rects

def GetHighWeightRect(rects, weights, num=2):
    select = []
    rects = list(rects)
    weights = list(weights)

    num = min(len(weights), num)

    for i in range(num):
        index = weights.index(max(weights))
        weights.remove(max(weights))
        select.append(rects[index])

    return select

def slice_window(img, H, W, padding):
    h, w = img.shape
    heigh = int((h-H)/padding)
    weigh = int((w-W)/padding)
    result = []
    for i in range(heigh):
        for j in range(weigh):
            x = i*padding
            y = j*padding
            result.append((x, y, x+H, y+W))
    
    return result

def DetectMymethod(img, H, W, clf):
    
    rects = []
    hog = cv2.HOGDescriptor((W, H), (16, 16), (8,8), (8,8), 9)

    for i in range(5):
        
        new_H = int(H * (3*(1.05**i)))
        new_W = int(W * (3*(1.05**i)))
        
        sw = slice_window(img, new_H, new_W, int(new_H/5))
        all_vec = []

        for (x1, y1, x2, y2) in sw:
            img2 = img[x1:x2, y1:y2]
            img2 = cv2.resize(img2, (W, H))
            vec = hog.compute(img2)
            vec = vec.flatten()
            all_vec.append(vec)

        pred = clf.predict(all_vec)

        for j, val in enumerate(pred):
            if val == 1:
                rects.append(sw[j])
    
    return rects

def DetectMymethod2(img, H, W, Scale, padding, clf):
    rects = []
    hog = cv2.HOGDescriptor((W, H), (16, 16), (8,8), (8,8), 9)

    new_H = int(H*Scale)
    new_W = int(W*Scale)

    sw = slice_window(img, new_H, new_W, padding)
    all_vec = []

    for (x1, y1, x2, y2) in sw:
        img2 = img[x1:x2, y1:y2]
        img2 = cv2.resize(img2, (W, H))
        vec = hog.compute(img2)
        vec = vec.flatten()
        all_vec.append(vec)

    pred = clf.predict(all_vec)

    for j, val in enumerate(pred):
            if val == 1:
                rects.append(sw[j])

    return rects

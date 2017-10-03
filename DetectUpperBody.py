import cv2
import numpy as np
import pickle
from utils import DetectMymethod2
from sklearn import svm

with open('./svm_model/upperbody64x40', 'rb') as fp:
    clf = pickle.load(fp)


W = 40
H = 64

hog = cv2.HOGDescriptor((W, H), (16, 16), (8,8), (8,8), 9)


def DetectUpperBody(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rect = DetectMymethod2(gray, H, W, 3.5, 30,  clf)
    
    return rect
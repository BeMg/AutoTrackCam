import cv2

def HOGdetect(img):
    HOG = cv2.HOGDescriptor()
    HOG.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    rects, weight = HOG.detectMultiScale(img)

    result = []

    for (x, y, w, h) in rects:
        result.append((x, y, x+w, y+h))

    return result
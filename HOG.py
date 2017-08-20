import numpy as np
import cv2
import math
from sklearn import svm
from sklearn.externals import joblib


class HOG:
    # 2 * 2 cell -> a block
    block_size = 2
    # 8 * 8 pixel -> a cell
    cell_size = 8
    nbin = 9
    h = 60
    w = 64
    clf = joblib.load('./svm_model/upperbody.pkl')
    padding = 10


    # ComputeGradient(img:2D-array)
    # Compute Greadient for
    # From a grayscale image to compute each cell gradient histogram.
    # Expecting to get (wight/cell_size) * (hight/cell_size) number gradient vector.
    def ComputeGradient(self, img):
        # The height and weight in image is reverse in numpy array.
        h,w = img.shape
        img = img.astype(float)
        grad = np.zeros(img.shape, dtype=(float,2))
        for i in range(h-2):
            for j in range(w-2):
                # The first element 
                dx = img[i][j]-img[i+2][j]
                dy = img[i][j]-img[i][j+2]
                mag = math.sqrt(dx*dx + dy*dy)
                mag = 1 if mag == 0 else mag
                grad[i][j] = (dy/mag, dx/mag)
        return grad
        
    # For each pixel, we compute the grad to angle, 
    # then collect angle into histogram for each cell. 
    def WeightVote(self, grad):
        h,w,_ = grad.shape
        h = int(h / self.cell_size)
        w = int(w / self.cell_size)
        cell_histogram = np.zeros((h, w, self.nbin))
        dest = 180 / self.nbin
        
        # For each cell
        for i in range(h):
            for j in range(w):
                # 0-180 degree divide to nbin
                histogram = np.zeros(self.nbin)
                # For each pixel in cell
                for k in range(self.cell_size):
                    for l in range(self.cell_size):
                        x = self.cell_size * i + k;
                        y = self.cell_size * j + l;
                        angle = np.arctan2(grad[x][y][1],grad[x][y][0]) / np.pi * 180
                        # !!! Have question about how to implemnt unsign angle
                        angle = angle if angle > 0 else -angle
                        
                        index = int(angle / dest)
                        offset = angle % dest
                        
                        if index == self.nbin or ((index == self.nbin-1) and (offset >= 10)):
                            histogram[self.nbin-1] += 1
                        elif index == 0 and offset < 10:
                            histogram[0] += 1
                        
                        else:
                            if offset >= 10:
                                offset -= 10
                                histogram[index] += (dest-offset)/dest
                                histogram[index+1] += offset/dest
                            else:
                                offset += 10
                                histogram[index] += (dest-offset)/dest
                                histogram[index-1] += offset/dest
                L2_norm = 0
                for val in histogram:
                    L2_norm += val*val
                L2_norm = np.sqrt(L2_norm)
            
                histogram = histogram/L2_norm
                cell_histogram[i][j] = histogram

        return cell_histogram
        
    def BlockCompute(self, histogram):
        h, w, _ = histogram.shape
        
        feature_vector = []

        for i in range(h-self.block_size+1):
            for j in range(w-self.block_size+1):
                for k in range(self.block_size):
                    for l in range(self.block_size):
                        x = i + k
                        y = j + l
                        feature_vector += list(histogram[x][y])

        return feature_vector
        
    # From img to compute a HOG descriptor
    def compute(self, img):
        grad = self.ComputeGradient(img)
        histogram = self.WeightVote(grad)
        fea_vec = self.BlockCompute(histogram)
        return fea_vec

    def detect(self, img):
        h, w = img.shape

        h2 = int((h-self.h)/self.padding)
        w2 = int((w-self.w)/self.padding)

        result = []

        for i in range(h2):
            for j in range(w2):
                x = i*self.padding
                y = j*self.padding
                crop_img = img[x:x+self.h, y:y+self.w]
                crop_HOG = self.compute(crop_img)
                pred = self.clf.predict([crop_HOG])      
                if pred == 1:
                    result.append((x,y,x+self.h, y+self.w))
        
        return result
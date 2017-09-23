import numpy as np

class Kalman(object):

    def __init__(self):

        self.state = None
        self.prestate = None
        self.measurement = np.ones((4, 1), dtype = np.float64)

        self.transitionMatrix = np.array(([ [1, 0, 1, 0], [0, 1, 0, 1], 
                                            [0, 0, 1, 0], [0, 0, 0, 1] ]), dtype = np.float64)
        self.measurementMatrix = np.eye(2, 4)
    
        self.processNoiceCov = np.eye(4, 4)
        self.measurementNoiceCov = np.array(([ [0.1, 0], [0, 0.1] ]), dtype = np.float64)

        self.predictMatrix = np.eye(4, 4)
        self.prePredictMatrix = np.eye(4, 4)
        self.correctMatrix = np.eye(4, 2)

    def predict(self):
        
        self.state = np.dot(self.transitionMatrix, self.prestate)
        self.predictMatrix = np.dot( np.dot(self.transitionMatrix, self.prePredictMatrix), self.transitionMatrix.transpose() ) + self.processNoiceCov
        
        return self.state
    def correct(self, measurement):
        
        preFitRes = measurement - np.dot(self.measurementMatrix, self.state)
        
        preFitResCov = np.dot( np.dot(self.measurementMatrix, self.predictMatrix), self.measurementMatrix.transpose() ) + self.measurementNoiceCov
        
        kalGain = np.dot( np.dot(self.predictMatrix, self.measurementMatrix.transpose()),np.linalg.inv(preFitResCov) )
        
        #Update

        self.state = self.state + np.dot(kalGain, preFitRes)
        
        self.predictMatrix = self.predictMatrix - np.dot( np.dot (kalGain, self.measurementMatrix), self.predictMatrix )

        #For k- 1 to k
        self.prestate = self.state
        
        self.prePredictMatrix = self.predictMatrix
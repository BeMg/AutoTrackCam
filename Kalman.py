import numpy as np

class Kalman(object):

    """
        Usage:

            init = np.array([[x1], [y1], [width], [length], [x_center], [y_center]], dtype = np.float64)
            kalman = Kalman(init)

            # Predict for k moment depends on k - 1 moment
            predict = kalman.predict() 

            #Correct filter by actual measurement in k moment and Prediction in k moment 
            measurement = np.array([[x1], [y1], [width], [length]], dtype = np.float64)
            kalman.correct(measurement)
            


    """
    def __init__(init):

        self.state = None
        self.prestate = init
        self.measurement = np.ones((4, 1), dtype = np.float64)

        self.transitionMatrix = np.array(([ [1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], 
                                            [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], 
                                            [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1]]), dtype = np.float64)
        self.measurementMatrix = np.eye(4, 6)
        
        self.processNoice = np.ones((6, 1))
        self.measurementNoice = np.array(([ [0.1], [0.1], [0], [0] ]), dtype = np.float64)

        self.processNoiceCov = np.eye(6, 6)
        self.measurementNoiceCov = np.array(([ [0.1, 0, 0, 0], [0, 0.1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0] ]), dtype = np.float64)

        self.predictMatrix = np.eye(6, 6)
        self.prePredictMatrix = np.eye(6, 6)
        self.correctMatrix = np.eye(6, 4)

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

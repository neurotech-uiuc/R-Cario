from . import classify as classify
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

from joblib import load

class GBDecisionTree(classify.Classifier):
    # TODO
    def __init__(self):
        return
    
    # TODO
    def train(self, trainingSets):
        return

    # TODO
    def saveModel(self, location):
        return

    def loadModel(self, location):
        self.model = load(location)

    def classify(self, observations):
        result = self.model.predict(observations)
        return result
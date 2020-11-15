from abc import ABC, abstractmethod # for abstract class

class Classifier(ABC):
    def __init__(self, modelfile):
        self.modelfile = modelfile
        super().__init__()

    # TrainingData -> Array of observations
    # Each observation is in the form (x,y,time,label)
    @abstractmethod
    def train(self, trainingData):
        pass

    @abstractmethod
    def classify(self, observation):
        pass


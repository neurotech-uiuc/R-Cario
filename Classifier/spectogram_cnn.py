import classify as classify


class SpectogramCNN(classify.Classifier):
    def train(self, trainingData):
        # print("Channel 0 Length:", len(trainingData[0][0][0]))
        # print("Channel 1 Length:", len(trainingData[1][0][0]))
        # print("Channel 2 Length:", len(trainingData[2][0][0]))

        # print("Channel 0 Obs Length in first observation:", len(trainingData[0][0][0][0]))
        # print("Channel 1 Obs Length first observation:", len(trainingData[1][0][0][0]))
        # print("Channel 2 Obs Length first observation:", len(trainingData[2][0][0][0]))

        spectogramFolders = trainingData[1]
        channel0Folder = spectogramFolders[0]
        
        

        pass

    def classify(self, observation):
        pass
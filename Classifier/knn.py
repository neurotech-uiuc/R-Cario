import classify as classify

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

class KNN(classify.Classifier):
    def __init__(self, n):
        self.model = KNeighborsClassifier(n_neighbors=n)

    def train(self, trainingSets):
        # make four empty numpy arrays
        X_train_all, X_test_all, y_train_all, y_test_all = np.array([[],[],[],[]])
        for trainingData in trainingSets:
      	# trainingData -> (c0, c1, c2) -> (x_groups, y_groups, t_groups), l_groups
          #  -> each group is 1 sec w 190 rows

            # channel_y: 3 channel list -> (? intervals, 190 recordings/interval)
            channel_y_list = [np.stack(channel[0][1]) for channel in trainingData.values()]

            # channel_data: (? intervals, 190 readings/interval, 3 channels)
            channel_data = np.stack(channel_y_list, axis=-1)
            
            # channel_means: (? meaned intervals, 3 channels)
            channel_means = channel_data.mean(axis=1)
            
            train_size = int(0.7*channel_means.shape[0])
            #means are normalized only on training data
            #labels across channels should be identical
            X = channel_means/channel_means[:train_size].std(axis=0)
            y = trainingData[0][1]
    
            
            X_train, X_test = np.split(X, [train_size])
            y_train, y_test = np.split(y, [train_size])

            np.append(X_train_all, X_train)
            np.append(X_test_all, X_test)
            np.append(y_train_all, y_train)
            np.append(y_test_all, y_test)

        
        self.model.fit(X_train_all, y_train_all)

        results = self.model.predict(X_test_all)
        accuracy = (results==y_test_all).mean()
        
        print(accuracy)

    def classify(self, observation):
        pass

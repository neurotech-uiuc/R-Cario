import classify as classify
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import numpy as np

class KNN(classify.Classifier):
    model = KNeighborsClassifier(n_neighbors=3)

    def train(self, trainingData):
      	# trainingData -> (c0, c1, c2) -> (x_groups, y_groups, t_groups), l_groups -> each group is 1 sec w 190 rows
        
        channel_0 = trainingData[0]
        channel_1 = trainingData[1]
        channel_2 = trainingData[2]
        
        
        y_0 = np.array([interval.mean() for interval in channel_0[0][1]])
        labels = channel_0[1]
        
        y_1 = np.array([interval.mean() for interval in channel_1[0][1]])
        # labels_1 = channel_1[1]
        
        y_2 = np.array([interval.mean() for interval in channel_2[0][1]])
        # labels_2 = channel_2[1]

        # shape: (?,3)=(intervals, channels)
        X = np.stack((y_0, y_1, y_2), axis=-1)
        # y = np.stack((labels_0, labels_1, labels_2), axis=-1)
        y = labels 
        
        X = np.mean(X, axis=1)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
        # print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
        # print((y_test[0]))
        model = KNeighborsClassifier(n_neighbors=3)
        model.fit(X_train.reshape(-1,1), y_train.reshape(-1,1))
        
        results = model.predict(X_test.reshape(-1,1))
        accuracy = (results == y_test).mean()
        print(accuracy)

    def classify(self, observation):
        return KNN.model.predict(KNN.y_train, KNN.y_test)

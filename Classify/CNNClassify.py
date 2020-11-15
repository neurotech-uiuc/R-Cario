import classify as classify
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D

import numpy as np

class CNN(classify.Classifier):
    def data_train(self, trainingData):
        # X forms the training data, and y forms the training labels
        X = np.array(trainingData.iloc[:, 1:])
        y = to_categorical(np.array(trainingData.iloc[:, 0]))

        # Split training data to sub-training (80%) and validation data (20%)
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=13)
        
        return X_train, X_val, y_train, y_val
        
    def convolute(X_train, X_val, y_train, y_val):
        cnn3 = Sequential()
        cnn3.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
        cnn3.add(MaxPooling2D((2, 2)))
        cnn3.add(Dropout(0.25))

        cnn3.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
        cnn3.add(MaxPooling2D(pool_size=(2, 2)))
        cnn3.add(Dropout(0.25))

        cnn3.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        cnn3.add(Dropout(0.4))

        cnn3.add(Flatten())

        cnn3.add(Dense(128, activation='relu'))
        cnn3.add(Dropout(0.3))
        cnn3.add(Dense(10, activation='softmax'))

        cnn3.compile(loss=keras.losses.categorical_crossentropy,
                      optimizer=keras.optimizers.Adam(),
                      metrics=['accuracy'])

        trained = cnn3.fit(X_train, y_train,
              batch_size=256,
              epochs=10,
              verbose=1,
              validation_data=(X_val, y_val))

        return trained

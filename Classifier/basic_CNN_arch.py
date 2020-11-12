import tensorflow as tf

from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

#split training data 


#Define Model
model = models.Sequential()
#input shape is the shape of each of the input images  (batch_size, height, width, depth), depth is color channels
model.add(layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(1920, 1440, 3)))
model.add(layers.MaxPooling2D(pool_size=(1, 3)))
model.add(layers.Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(1, 2)))
#model.add(layers.Dropout(0.25))
model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu'))
#model.add(layers.Dropout(0.5))
#num classes refers to how many labels we have, like right foot tap, left foot tap, etc
model.add(layers.Dense(5, activation='softmax'))
#Compile
model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), optimizer='adam', metrics=['accuracy'])
print(model.summary())
#Train and Test The Model
#model.fit(x_train, y_train, batch_size=4, epochs=10, verbose=1, validation_data=(x_test, y_test))
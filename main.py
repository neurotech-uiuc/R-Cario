# Pseudocode:

"""

    -- import the neccasary components -- 

    import Classifier as Classifier
    import RC_Controller as RC_Controller
    import RealTime_Capture as EEG

    model = Classifier.load(model="KNN")

    #if the below code takes longer than 500ms to run, 
    # either increase interval 
    # or make each iteration run in the background so it doesnt delay the next
    every 2 seconds: 
        # read stream should always return the same number of data points
        input = eeg.read_stream("1 second")
        outputLabel = model.classify(input)
        RC_Controller.sendSignal(outputLabel)


"""
from Classifier import knn as knn
from Training import Datacreate as dc
import numpy as np
from RealTime_Capture import Capture as capt
from RC_Controller import Controller as contr

import time

#setup capture module
serialPort = "/dev/cu.usbmodem11"
EEG = capt.Capture(1, serialPort)

# init base
print("LOADING MODEL")
model = knn.KNN(3)
model.loadModel("combinedKNN")
print("LOADED MODEL")

#init controller
# controller = contr.Controller(9600, '/dev/cu.HC-06-SPPDev')
# controller.connect()

print("ATTEMPT START STREAM")
EEG.startStream()
for i in range(20): # change this loop condition to while flag 
    NUM_SAMPLES = 190
    data = EEG.getData(2, NUM_SAMPLES)
    print("Data:\n", data)
    action = model.classify(data)
    print(action)
    # controller.sendAction(action)

# controller.close()

EEG.closeStream()
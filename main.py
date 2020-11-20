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
    every 500ms: 
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

#setup capture module
serialPort = "/dev/cu.usbmodem11"
EEG = capt.Capture(1, serialPort)

# init base
model = knn.KNN(3)
model.loadModel("combinedKNN")

#init controller
controller = contr.Controller("port")

EEG.startStream()
for i in range(100): # change this loop condition to while flag 
    NUM_SAMPLES = 190
    data = EEG.getData(1, NUM_SAMPLES)
    action = model.classify(data)
    print(action)
    controller.sendAction(action)


# LeftEye_path = "../Recordings/Fall_2020/OpenBCISession_2020-10-11_16-33-50-YAN-LEFT-EYE/OpenBCI-RAW-2020-10-11_16-38-59.txt"
# LeftEye_label_path = "../Recordings/Labels/yanLeftEye"
# LeftEye_observations = dc.getObservationSet(
#     LeftEye_path, LeftEye_label_path, 1000, [0, 1, 2], 'L_EYE')


# chan0 = LeftEye_observations[0][0][1]
# chan1 = LeftEye_observations[1][0][1]
# chan2 = LeftEye_observations[2][0][1]

# obs = np.array([chan0[0], chan1[0], chan2[0]])

# # print(model.classify(obs))

# # one_obs = np.array([LeftEye_observations[]


# channel_y_list = [np.stack(channel[0][1]) for channel in LeftEye_observations.values()]

# # channel_data: (? intervals, 190 readings/interval, 3 channels)
# channel_data = np.stack(channel_y_list, axis=-1)

# # channel_means: (? meaned intervals, 3 channels)
# channel_means = channel_data.mean(axis=1)

# train_size = int(0.5*channel_means.shape[0])
# # means are normalized only on training data
# # labels across channels should be identical

# print(channel_means[:train_size].std(axis=0))
# X = (channel_means/channel_means[:train_size].std(axis=0))[0]
# print(X)

# print(obs.mean(axis=1)/obs.std(axis=1))

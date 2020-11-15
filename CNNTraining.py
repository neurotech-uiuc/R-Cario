from keras.datasets import mnist

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../Classifier/')
import Datacreate as dc

#import CNNClassify as model

RightFoot_path = "../../Recordings/Fall_2020/OpenBCISession_2020-10-11_16-26-10-YAN-RIGHT-FOOT/OpenBCI-RAW-2020-10-11_16-26-50.txt"
RightFoot_label_path = "../../Recordings/Labels/yanRightFoot"

LeftFoot_path = "../Recordings/Fall_2020/OpenBCISession_2020-10-11_16-00-28-YAN-LEFT-FOOT/OpenBCI-RAW-2020-10-11_16-01-30.txt"
LeftFoot_label_path = "../Recordings/Labels/yanLeftFoot.txt.txt"

RightEye_path = "../Recordings/Fall_2020/OpenBCISession_2020-10-11_16-58-40-YAN-RIGHT-EYE/OpenBCI-RAW-2020-10-11_16-59-03.txt"
RightEye_label_path = "../Recordings/Labels/yanRightEye"

LeftEye_path = "../Recordings/Fall_2020/OpenBCISession_2020-10-11_16-33-50-YAN-LEFT-EYE/OpenBCI-RAW-2020-10-11_16-38-59.txt"
LeftEye_label_path = "../Recordings/Labels/yanLeftEye"

RightFoot_observations = dc.getObservationSet(RightFoot_path, RightFoot_label_path, 1000, [0,1,2])
LeftFoot_observations = dc.getObservationSet(LeftFoot_path, LeftFoot_label_path, 1000, [0,1,2])
RightEye_observations = dc.getObservationSet(RightEye_path, RightEye_label_path, 1000, [0,1,2])
LeftEye_observations = dc.getObservationSet(LeftEye_path, LeftEye_label_path, 1000, [0,1,2])

combined = pd.DataFrame({RightFoot_observations, LeftFoot_observations, RightEye_observations, LeftEye_observations})

cnn = CNN("modelFile")
X_train, X_val, y_train, y_val = cnn.data_train(combined)
trained = cnn.convolute(X_train, X_val, y_train, y_val)

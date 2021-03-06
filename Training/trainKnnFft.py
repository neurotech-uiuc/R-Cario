import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../Classifier/')
import Datacreate as dc

import knn_fft as model
# import trainExample as trainer

RightFoot_path = "../Recordings/Fall_2020/OpenBCISession_2020-10-11_16-26-10-YAN-RIGHT-FOOT/OpenBCI-RAW-2020-10-11_16-26-50.txt"
RightFoot_label_path = "../Recordings/Labels/yanRightFoot"

LeftFoot_path = "../Recordings/Fall_2020/OpenBCISession_2020-10-11_16-00-28-YAN-LEFT-FOOT/OpenBCI-RAW-2020-10-11_16-01-30.txt"
LeftFoot_label_path = "../Recordings/Labels/yanLeftFoot.txt.txt"

RightEye_path = "../Recordings/Fall_2020/OpenBCISession_2020-10-11_16-58-40-YAN-RIGHT-EYE/OpenBCI-RAW-2020-10-11_16-59-03.txt"
RightEye_label_path = "../Recordings/Labels/yanRightEye"

LeftEye_path = "../Recordings/Fall_2020/OpenBCISession_2020-10-11_16-33-50-YAN-LEFT-EYE/OpenBCI-RAW-2020-10-11_16-38-59.txt"
LeftEye_label_path = "../Recordings/Labels/yanLeftEye"

RightFoot_observations = dc.getObservationSet(RightFoot_path, RightFoot_label_path, 1000, [0,1,2], 'R_FOOT')
LeftFoot_observations = dc.getObservationSet(LeftFoot_path, LeftFoot_label_path, 1000, [0,1,2], 'L_FOOT')
RightEye_observations = dc.getObservationSet(RightEye_path, RightEye_label_path, 1000, [0,1,2], 'R_EYE')
LeftEye_observations = dc.getObservationSet(LeftEye_path, LeftEye_label_path, 1000, [0,1,2], 'L_EYE')

knn_fft = model.KNN_FFT(3)
# knn_fft.train([RightFoot_observations, LeftFoot_observations, RightEye_observations, LeftEye_observations])
knn_fft.train([RightFoot_observations])
knn_fft.train([RightFoot_observations])
knn_fft.train([RightFoot_observations])

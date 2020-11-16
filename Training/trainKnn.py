import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../Classifier/')
import Datacreate as dc
import DataCreateNew as dcNew

import knn as model
import knnGrouped as knnGrouped
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

steveLF_path = "../../Recordings/steve/OpenBCISession_2020-11-14_18-04-28-steve-lf200/OpenBCI-RAW-2020-11-14_18-05-09.txt"
steveLF_lablels = "../../Recordings/steve_time/stevenLeftFoot200"

steveLF_path = "../../Recordings/steve/OpenBCISession_2020-11-14_18-04-28-steve-lf200/OpenBCI-RAW-2020-11-14_18-05-09.txt"
steveLF_lablels = "../../Recordings/steve_time/stevenLeftFoot200"

base = "../../Recordings/steve/"
baseTime = "../../Recordings/steve_time/"

steveRF_path = base + "OpenBCISession_2020-11-14_17-57-45-steve-rf/OpenBCI-RAW-2020-11-14_17-58-23.txt"
steveRF_labels = baseTime + "stevenRightFoot"

# steveLE_path = base + "OpenBCISession_2020-11-14_17-57-45-steve-rf/OpenBCI-RAW-2020-11-14_17-58-23.txt"
# steveLE_labels = baseTime + "stevenRightFoot"

steveRE_path = base + "OpenBCISession_2020-11-14_18-16-22-steve-re/OpenBCI-RAW-2020-11-14_18-17-03.txt"
steveRE_labels = baseTime + "stevenrighteye"

steveLF_observations = dcNew.getObservationSet(steveLF_path, steveLF_lablels, 1000, [0,1,2], 'L_FOOT')
steveRF_observations = dcNew.getObservationSet(steveRF_path, steveRF_labels, 1000, [0,1,2], 'R_FOOT')
steveRE_observations = dcNew.getObservationSet(steveRE_path, steveRE_labels, 1000, [0,1,2], 'R_EYE')


# USING AVERAGE VALUE
# knn = model.KNN(3)
# print("Steven-> [No Action, L_FOOT, R_FOOT, R_EYE")
# knn.train([steveLF_observations, steveRF_observations, steveRE_observations])

# print("Yan-> [No Action, L_FOOT, R_FOOT, L_EYE, R_EYE")
# knn.train([RightFoot_observations, LeftFoot_observations, RightEye_observations, LeftEye_observations])

# print("COMBINED")
# knn.train([steveLF_observations, steveRF_observations, steveRE_observations, RightFoot_observations, LeftFoot_observations, RightEye_observations, LeftEye_observations])

# USING GROUPING
knn = knnGrouped.KNN(3)
print("Steven-> [No Action, L_FOOT, R_FOOT, R_EYE")
knn.train([steveLF_observations, steveRF_observations, steveRE_observations])

print("Yan-> [No Action, L_FOOT, R_FOOT, L_EYE, R_EYE")
knn.train([RightFoot_observations, LeftFoot_observations, RightEye_observations, LeftEye_observations])

print("COMBINED")
knn.train([steveLF_observations, steveRF_observations, steveRE_observations, RightFoot_observations, LeftFoot_observations, RightEye_observations, LeftEye_observations])

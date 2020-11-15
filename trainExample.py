# In this file, I will train the example model with some fake data
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../Classifier/')
import Datacreate as dc

import example as model
# import trainExample as trainer

path = "../../Recordings/Fall_2020/OpenBCISession_2020-10-11_16-26-10-YAN-RIGHT-FOOT/OpenBCI-RAW-2020-10-11_16-26-50.txt"
label_path = "../../Recordings/Labels/yanRightFoot"

exampleModel = model.Example("modelFile")
observations = dc.getObservationSet(path, label_path, 1000, [0,1,2])
exampleModel.train(observations)



import classify as classify
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from Datacreate import getObservationSet


class knn_channel_grouping_model(classify.Classifier):
    

    # trainingData is a map of each label to its observationSet (defined in Datacreate.getObservationSet())
    def train(self, trainingData):

        pass
        
    def classify(self, observation):

        
        pass

recordingHeader = "Recordings/Fall_2020/"
labelHeader = "Recordings/Labels/"

recordings = ["OpenBCISession_2020-10-11_16-00-28-YAN-LEFT-FOOT/OpenBCI-RAW-2020-10-11_16-01-30",
"OpenBCISession_2020-10-11_16-26-10-YAN-RIGHT-FOOT/OpenBCI-RAW-2020-10-11_16-26-50",
"OpenBCISession_2020-10-11_16-33-50-YAN-LEFT-EYE/OpenBCI-RAW-2020-10-11_16-38-59",
"OpenBCISession_2020-10-11_16-58-40-YAN-RIGHT-EYE/OpenBCI-RAW-2020-10-11_16-59-03"]
labels = ["yanLeftFoot.txt.txt", "yanRightFoot", "yanLeftEye", "yanRightEye"]

# observationSets: map of each label to its observation set
# each observation set is a map of each channel to its observations
# each observation is a tuple ((x_groups, y_groups, t_groups), l_groups)

observationSets = {}
for i, label in enumerate(labels):
    observationSets[label] = getObservationSet(recordingHeader + recordings[i] + ".txt", labelHeader + labels[i], 1000, [0, 1, 2])

# x = observationSets["yanRightFoot"][0]
# print(x[0][0].shape, x[0][1].shape, x[0][2].shape, x[1].shape)
# print(x[0][0][0].shape, x[0][1][0].shape, x[0][2][0].shape)

y_groups_grid = [[observationSets[label][i][0][1][:150] for i in range(3)] for label in labels]
l_groups_grid = [[observationSets[label][i][1][:150] for i in range(3)] for label in labels]
vec_size = 3 * 190

data = np.array([])
answers = []

t_y_groups_grid = [[y_groups_grid[i][j][l_groups_grid[i][j]] for j in range(3)] for i in range(4)]

for i,y_groups_list in enumerate(t_y_groups_grid):
    for obs_num in range(y_groups_list[0].shape[0]):
        vec = np.array([y_groups_list[0][obs_num], y_groups_list[1][obs_num], y_groups_list[2][obs_num]]).T.flatten()

        data = np.append(data, vec)
        if l_groups_grid[i][0][obs_num] == 0:
            answers.append("NONE")
        else:
            answers.append(labels[i])

data = data.reshape(int(data.size / vec_size), vec_size)

classifier = KNeighborsClassifier(n_neighbors=5)
classifier.fit(data, answers)

# model = knn_channel_grouping_model()
# model.train(observationSet)
# print((l_groups_grid[0][0] == l_groups_grid[0][1]), (l_groups_grid[0][0] == l_groups_grid[0][2]))




# test_y_groups_grid = [[y_groups_grid[i][j][l_groups_grid[i][j]] for j in range(3)] for i in range(4)]
test_data = np.array([])
test_answers = []

test_y_groups_grid = [[observationSets[label][i][0][1][150:] for i in range(3)] for label in labels]
test_l_groups_grid = [[observationSets[label][i][1][150:] for i in range(3)] for label in labels]

for i,test_y_groups_list in enumerate(test_y_groups_grid):
    for obs_num in range(test_y_groups_list[0].shape[0]):
        vec = np.array([test_y_groups_list[0][obs_num], test_y_groups_list[1][obs_num], test_y_groups_list[2][obs_num]]).T.flatten()

        test_data = np.append(test_data, vec)
        if test_l_groups_grid[i][0][obs_num] == 0:
            test_answers.append("NONE")
        else:
            test_answers.append(labels[i])

test_data = test_data.reshape(int(test_data.size / vec_size), vec_size)

prediction = classifier.kneighbors(test_data, return_distance=False)
# prediction = classifier.predict(test_data)
gross_predictions = [[answers[i] for i in p] for p in prediction]
predictions = []

for gp in gross_predictions:
    none_count = 0
    for i in gp:
        if i == 'NONE':
            none_count += 1
    if none_count != len(gp):
        for i in gp:
            if i != 'NONE':
                predictions.append(i)
                break
        continue
    predictions.append('NONE')

# accuracy = 0
# for i in range(len(prediction)):
#     if (prediction[i] == test_answers[i]):
#         accuracy += 1
# print("Accuracy: ", accuracy / len(prediction))

print(confusion_matrix(test_answers, predictions, labels=["NONE", "yanLeftFoot.txt.txt", "yanRightFoot", "yanLeftEye", "yanRightEye"], normalize='true'))
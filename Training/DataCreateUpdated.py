import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.fft import fft
from string import digits
from datetime import datetime, timedelta
import requests

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

# define example
labels = {'NONE' : 0,  'JAW_CLENCH' : 1, 'F_HEAD' : 2, 'L_EYE' : 3, 'R_EYE' : 4}
labelInts = np.array([0, 1, 2, 3, 4])
# integer encode
label_encoder = LabelEncoder()
integer_encoded = label_encoder.fit_transform(labelInts)
# binary encode
onehot_encoder = OneHotEncoder(sparse=False)
integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
onehot_encoded = onehot_encoder.fit_transform(integer_encoded)

def getOneHot(label):
	return onehot_encoded[labels[label]]

def getOneHotLabels():
	output = {}
	for label in labels:
		output[label] = getOneHot(label)
	return output
	
def getTitle(recordingFile):
	return recordingFile.split("-")[-1].split(".")[0].translate({ord(k): None for k in digits})

# pass none if dont want granularity
# pass none to dataLimit if want all the data
def getData(path, granularity, channels, dataLimit):
	dataRaw = []
	dataStartLine = 6
	count = 0
	with open(path, 'r') as data_file:
		for line in data_file:
			if count >= dataStartLine:
					dataRaw.append(line.strip().split(','))
			else:
					count += 1
	dataRaw = np.char.strip(np.array(dataRaw))

	dataChannels = dataRaw[:, 1:5]
	timeChannels = dataRaw[:, 15]

	if granularity is None:
		granularity = 1
	# the current channel of data
	if dataLimit is None:
		dataLimit = len(dataChannels)

	channelData = dataChannels[:,channels][:dataLimit:granularity].transpose()
	y_channels = channelData.astype(float)
	inds = np.arange(channelData.shape[1])
	t = np.array([datetime.strptime(time[11:],'%H:%M:%S.%f') for time in timeChannels])
	return y_channels,inds,t

def getLabel(path):
	dataRaw = []
	first = True
	basetime = None
	with open(path, 'r') as label_file:
		for line in label_file:
			if(first):
				dt_obj = datetime.strptime(line[11:].strip(),'%H:%M:%S.%f')
				basetime = dt_obj
				# dataRaw.append(dt_obj)
				first = False
			else:
				dr = np.char.strip(np.array(line[1:-1].split(", ")))
				# print(dr)
				for i in range(len(dr)):
					if dr[i] == '1':
						dataRaw.append(basetime + timedelta(seconds=i))
	# print(dataRaw)
	return dataRaw

	
def groupbyInterval(data, labels, interval, actionType):
	#data tuple (x,y,z). labels: datetimes. interval(ms): int
	y_channels,inds,t = data
	interval_ms = timedelta(milliseconds=interval)
	
	split_inds = []
	cutoff_times = [t[0]+interval_ms]
	for ind in range(t.shape[0]):
		time = t[ind]
		if time >= cutoff_times[-1]:
			split_inds.append(ind)
			cutoff_times.append(cutoff_times[-1] + interval_ms)
	
	ind_groups = np.split(inds, split_inds)
	y_channels_groups = np.split(y_channels, split_inds, axis=1)
	t_groups = np.split(t, split_inds)

	#find min group size
	min_group_size = ind_groups[0].shape[0]
	for i in range(len(split_inds)-1):
		if ind_groups[i].shape[0] < min_group_size:
			min_group_size = ind_groups[i].shape[0]

	#rectangularize jagged arrays
	for i in range(len(split_inds)):
		ind_groups[i] = ind_groups[i][:min_group_size]
		y_channels_groups[i] = y_channels_groups[i][:,:min_group_size]
		t_groups[i] = t_groups[i][:min_group_size]

	#drop short last group
	ind_groups = np.array(ind_groups[:-1])
	y_channels_groups = np.array(y_channels_groups[:-1]).transpose((1,0,2))
	t_groups = np.array(t_groups[:-1])

	#assign labels to groups
	NO_ACTION = 0
	ACTION = 1

	if actionType:
		NO_ACTION = getOneHot("NONE")
		ACTION = getOneHot(actionType)
		
	l_groups = np.array([NO_ACTION] * ind_groups.shape[0])
	
	lnum=0
	for ind in range(len(cutoff_times)):
		if lnum==len(labels):
			break

		cutoff_time = cutoff_times[ind]
		if labels[lnum] < cutoff_time:
			l_groups[ind] = ACTION
			lnum+=1
	
	return y_channels_groups, ind_groups, t_groups, l_groups


#THIS IS THE MAIN METHOD FOR INTERACTION
# Inputs:
# datafile, labelfile, interval, channels requested
def getObservations(dataPath, labelPath, interval, channels, actionType):
	data = getData(dataPath, None, channels, None)
	action_times = getLabel(labelPath)
	observations = groupbyInterval(data, action_times, interval, actionType)
	
	return observations







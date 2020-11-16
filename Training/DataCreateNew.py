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
labels = {'NONE' : 0,  'L_FOOT' : 1, 'R_FOOT' : 2, 'L_EYE' : 3, 'R_EYE' : 4}
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
def getData(path, granularity, channel, dataLimit):

	dataRaw = []
	dataStartLine = 6
	count = 0
	for line in open(path, 'r').readlines(): 
			if count >= dataStartLine:
					dataRaw.append(line.strip().split(','))
			else:
					count += 1
	dataRaw = np.char.strip(np.array(dataRaw))

	# print(dataRaw[0])
	dataChannels = dataRaw[:, 1:5]
	timeChannels = dataRaw[:, 14]

	if granularity is None:
		granularity = 1
	# the current channel of data
	if dataLimit is None:
		dataLimit = len(dataChannels)

	channelData = dataChannels[:,channel][:dataLimit:granularity]
	y = channelData.astype(float)
	x = np.arange(len(channelData))
	t = [datetime.strptime(time.split()[1],'%H:%M:%S.%f') for time in timeChannels]
	return x,y,t

def getLabel(path):
	dataRaw = []
	with open(path, 'r') as label_file:
		for line in label_file:
			dt_obj = datetime.strptime(line.strip(),'%H:%M:%S.%f')
			dataRaw.append(dt_obj)
	return dataRaw
	
		
	
def groupbyInterval(data, labels, interval, actionType):
	#data tuple (x,y,z). labels: datetimes. interval(ms): int
	x,y,t = data
	interval_ms = timedelta(milliseconds=interval)
	
	split_inds = []
	cutoff_times = [t[0]+interval_ms]
	for ind in range(len(t)):
		time = t[ind]
		if time >= cutoff_times[-1]:
			split_inds.append(ind)
			cutoff_times.append(cutoff_times[-1] + interval_ms)
	
	x_groups = np.array(np.split(x, split_inds))
	y_groups = np.array(np.split(y, split_inds))
	t_groups = np.array(np.split(t, split_inds))
	# l_groups = np.zeros(len(x_groups), dtype=bool)

	NO_ACTION = 0
	ACTION = 1

	if actionType:
		NO_ACTION = getOneHot("NONE")
		ACTION = getOneHot(actionType)
		
	l_groups = np.array([NO_ACTION] * len(x_groups))
	
	lnum=0
	for ind in range(len(cutoff_times)):
		if lnum==len(labels):
			break

		cutoff_time = cutoff_times[ind]
		if labels[lnum] < cutoff_time:
			l_groups[ind] = ACTION
			lnum+=1
	
	return (x_groups, y_groups, t_groups), l_groups


def return_millisecond_timestamps(labels):
	#return 1 or 0
	x = []
	for timestamp in labels:
		dt_obj = datetime.strptime(timestamp,'%H:%M:%S.%f')
		millisec = dt_obj.timestamp()*1000
				
		x.append(millisec)
	
	return x


def standardise_observations(grouped_data, group_contains_label):

	REQ_NUM_PTS = 190

	x_groups,y_groups,t_groups = grouped_data
	l_groups = group_contains_label

	#remove all instances where not enough sample pints
	i = 0
	while i < len(y_groups):
		if len(y_groups[i]) < REQ_NUM_PTS:
			x_groups = np.delete(x_groups, i)
			y_groups = np.delete(y_groups, i)
			t_groups = np.delete(t_groups, i)
			l_groups = np.delete(l_groups, i, 0)
		else:
			i = i+1

	# limit to required observations
	for i in range(len(x_groups)):
		x_groups[i] = x_groups[i][:REQ_NUM_PTS]
		y_groups[i] = y_groups[i][:REQ_NUM_PTS]
		t_groups[i] = t_groups[i][:REQ_NUM_PTS]

	return (x_groups, y_groups, t_groups), l_groups

#THIS IS THE MAIN METHOD FOR INTERACTION
# Inputs:
# datafile, labelfile, interval, channels requested
def getObservationSet(dataPath, labelPath, interval, channels, actionType):
	observationSet = {}
	for channel in channels:
		data = getData(dataPath, None, channel, None)
		action_times = getLabel(labelPath)
		observations = groupbyInterval(data, action_times, interval, actionType)
		observations = standardise_observations(observations[0], observations[1])
		observationSet[channel] = observations
	
	return observationSet






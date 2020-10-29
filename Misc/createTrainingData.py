import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.fft import fft
from string import digits
from datetime import datetime, timedelta
import requests

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

	dataChannels = dataRaw[:, 1:5]
	timeChannels = dataRaw[:, 8]

	if granularity is None:
		granularity = 1
	# the current channel of data
	if dataLimit is None:
		dataLimit = len(dataChannels)

	channelData = dataChannels[:,channel][:dataLimit:granularity]
	y = channelData.astype(float)
	x = np.arange(len(channelData))
	t = [datetime.strptime(time,'%H:%M:%S.%f') for time in timeChannels]
	return x,y,t

def getLabel(path):
	dataRaw = []
	with open(path, 'r') as label_file:
		for line in label_file:
			dt_obj = datetime.strptime(line.strip(),'%H:%M:%S.%f')
			dataRaw.append(dt_obj)
	return dataRaw
	
		
	
def groupbyInterval(data, labels, interval):
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
	l_groups = np.zeros(len(x_groups), dtype=bool)
	
	lnum=0
	for ind in range(len(cutoff_times)):
		if lnum==len(labels):
			break

		cutoff_time = cutoff_times[ind]
		if labels[lnum] < cutoff_time:
			l_groups[ind] = 1
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

		
def fftData(x, y, N):
	# https://docs.scipy.org/doc/scipy/reference/tutorial/fft.html
	# N = frequency limiter
	if N == None:
		N = len(x)

	# sample spacing
	T = 0.005
	# x = np.arange(len(channel))
	# y = channel0.astype(float)
	yf = fft(y)
	xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
	return xf, yf, N


def standardise_observations(grouped_data, group_contains_label):
	x_groups,y_groups,t_groups = grouped_data
	l_groups = group_contains_label

	i = 0
	while i < len(y_groups):
		if len(y_groups[i]) < 190:
			x_groups = np.delete(x_groups, i)
			y_groups = np.delete(y_groups, i)
			t_groups = np.delete(t_groups, i)
			l_groups = np.delete(l_groups, i)
		else:
			i = i+1

	for i in range(len(x_groups)):
		x_groups[i] = x_groups[i][:190]
		y_groups[i] = y_groups[i][:190]
		t_groups[i] = t_groups[i][:190]

	return (x_groups, y_groups, t_groups), l_groups

channel = 0

# plotFFT(rawDataLocs[0], 0)
path = "../Recordings/Fall_2020/OpenBCISession_2020-10-11_16-26-10-YAN-RIGHT-FOOT/OpenBCI-RAW-2020-10-11_16-26-50.txt"
label_path = "../Recordings/Labels/yanRightFoot"

interval = 1000
data = getData(path, None, channel, None)
action_times = getLabel(label_path)
#grouped_data: (x_groups, y_groups, t_groups)
grouped_data, group_contains_label = groupbyInterval(data, action_times, interval)
# grouped_data[2][group_contains_label][0]

grouped_data, group_contains_label = standardise_observations(grouped_data, group_contains_label)


y_groups = grouped_data[1]
t_groups = grouped_data[2]
l_groups = group_contains_label


# print((y_groups))
# print(len(l_groups))

#actionOccured = y_groups[l_groups]
#noActionOccured = y_groups[~l_groups]

actionOccured = y_groups[l_groups]
noActionOccured = y_groups[np.logical_not(l_groups)]

# print(len(actionOccured))
# print(len(noActionOccured))

# print(l_groups)

avgActionSum = 0
avgActionCount = 0

avgNoActionSum = 0
avgNoActionCount = 0

stdActionSum = 0
stdNoActionSum = 0

actionAvgs = []
noActionAvgs = []

actions = np.array([])
for action in actionOccured:
	actions = np.concatenate((actions, action))

noActions = np.array([])
for action in noActionOccured:
	noActions = np.concatenate((noActions, action))

for action in actionOccured:
	avgActionSum += np.sum(action)
	avgActionCount += len(action)
	actionAvgs.append(action.mean())
	

for action in noActionOccured:
	avgNoActionSum += np.sum(action)
	avgNoActionCount += len(action)
	#stdNoActionSum += np.std(action)
	noActionAvgs.append(action.mean())
	
actionAvgsArr = np.array(actionAvgs)
noActionAvgsArr = np.array(noActionAvgs)

print("Average Action of Channel 0: ", actionAvgsArr.mean())
print("Average No Action of Channel 0: ", noActionAvgsArr.mean())
#print("Average Action std of Channel 0: ", stdActionSum / len(actionOccured))
#print("Average No Action std of Channel 0: ", stdActionSum / len(noActionOccured))

print("Std of Avgs of Channel 0: ", np.std(actionAvgsArr))
print("Std of Avgs of Channel 0: ", np.std(noActionAvgsArr))
# print(noActionOccured)

# for obs in y_groups:
# 	print(len(obs))

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



# plotFFT(rawDataLocs[0], 0)
path = "../Recordings/Fall_2020/OpenBCISession_2020-10-11_16-00-28-YAN-LEFT-FOOT/OpenBCI-RAW-2020-10-11_16-01-30.txt"
label_path = "../Recordings/Labels/yanLeftFoot.txt.txt"
interval = 1000
data = getData(path, None, 0, None)
action_times = getLabel(label_path)
#grouped_data: (x_groups, y_groups, t_groups)
grouped_data, group_contains_label = groupbyInterval(data, action_times, interval)
grouped_data[2][group_contains_label][0]
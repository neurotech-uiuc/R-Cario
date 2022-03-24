# 1. Convert first line to date time
# 2. Read binary array
# 3. Read formatted array
# 4. Get timestamps
# 5. For each timestamp, convert to a number corresponding to the index of the interval
# 6. Label accordingly  


import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.fft import fft
from string import digits
from datetime import datetime, timedelta
import requests
import math

def labelLine(line, labels, startTime):
    time = datetime.fromisoformat(line[len(line)-1])
    duration = time - startTime
    seconds = duration.total_seconds()
    line.append(seconds)
    line.append(labels[int(seconds)])
    if (time < startTime):
        return none

    print(time)

    return line


def getData(path,labels,startTime):
    data = []
    count = 0
    # Gets difference between startTime and time of first data point and eventually subtracts that difference from the data points
    startTimeDelta = 0
    for line in open(path, 'r').readlines(): 
        if count >= 5:
            lineArr = []
            for x in (line.strip().split(',')):
               lineArr.append(x.strip())
            # here is where it computes the difference
            if (count == 5):
                time = datetime.fromisoformat(lineArr[len(lineArr)-1])
                startTimeDelta = time - startTime
            lineArr = labelLine(lineArr,labels,startTime)
            if (lineArr != None):
                data.append(lineArr)
        else:
            count += 1
    
    return data

    


def getLabels(path):
    date = ""
    dataRaw = []
    count = 0
    for line in open(path, 'r').readlines(): 
        if count >= 1:
            for x in (line.strip().split(',')):
                dataRaw.append(x.replace("[","").replace("]",""))
                count += 1

                
        else:
            date = line.strip()
            count += 1


    realDate = datetime.fromisoformat(date)
    dataRaw = np.char.strip(np.array(dataRaw))
    print(realDate)
    for x in dataRaw:
        print(x)

    data = []
    data.append(realDate)
    data.append(dataRaw)
    print(count-1)
    return data

data = getLabels("JawClench_labels_Ansh_12-02-21-1918.txt")
startTime = data[0]
labels = data[1]
data = getData("OpenBCI-RAW-2021-12-02_19-19-53.txt",labels,startTime)

print(data[1][len(data[0])-1])



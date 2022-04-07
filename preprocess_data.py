import numpy as np

def getMeanAbsDeviation(dchannel):
    return np.transpose(np.mean(np.abs(dchannel - np.mean(dchannel, axis=2, keepdims=True)), axis=2))

def getMeanSquaredDeviation(dchannel):
    return np.transpose(np.mean(np.square(dchannel - np.mean(dchannel, axis=2, keepdims=True)), axis=2))

def getMean(dchannel):
    return np.transpose(np.mean(dchannel, axis=2))

def getPercentile(dchannel, percent):
    return np.transpose(np.percentile(dchannel, percent, axis=2))

def getPercentile10(dchannel, percent=10):
    return np.transpose(np.percentile(dchannel, percent, axis=2))

def getPercentile90(dchannel, percent=90):
    return np.transpose(np.percentile(dchannel, percent, axis=2))

def getPercentile15(dchannel, percent=15):
    return np.transpose(np.percentile(dchannel, percent, axis=2))

def getPercentile85(dchannel, percent=85):
    return np.transpose(np.percentile(dchannel, percent, axis=2))

def getPercentile5(dchannel, percent=5):
    return np.transpose(np.percentile(dchannel, percent, axis=2))

def getPercentile95(dchannel, percent=95):
    return np.transpose(np.percentile(dchannel, percent, axis=2))

def getSpread(dchannel):
    return np.transpose(np.max(dchannel, axis=2) - np.min(dchannel, axis=2))

def getSpreadPercentile(dchannel, low=5, high=95):
    return getPercentile(dchannel, high) - getPercentile(dchannel, low)

def pre_process(y_channels_groups, mean, stdev):
    functsList = [getMean, getMeanSquaredDeviation, getMeanAbsDeviation, getSpreadPercentile, getPercentile10, getPercentile90]
    fX = None
    for funct in functsList:
        if fX is not None:
            fX = np.concatenate((fX, funct(y_channels_groups)), axis=1)
        else:
            fX = funct(y_channels_groups)
    return (fX - mean)/stdev

def callibration(y_channels_groups):
    functsList = [getMean, getMeanSquaredDeviation, getMeanAbsDeviation, getSpreadPercentile, getPercentile10, getPercentile90]
    fX = None
    for funct in functsList:
        if fX is not None:
            fX = np.concatenate((fX, funct(y_channels_groups)), axis=1)
        else:
            fX = funct(y_channels_groups)
    mean = np.mean(fX, axis=0)
    stdev = np.std(fX, axis=0)
    return mean, stdev
        
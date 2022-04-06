import numpy as np
from FeatureExtractFunctions import getMean, getMeanSquaredDeviation, getMeanAbsDeviation, getSpreadPercentile, getPercentile10, getPercentile90

functsList = [getMean, getMeanSquaredDeviation, getMeanAbsDeviation, getSpreadPercentile, getPercentile10, getPercentile90]

def pre_process(y_channels_groups, mean, stdev):
    fX = None
    for funct in functsList:
        if fX is not None:
            fX = np.concatenate((fX, funct(y_channels_groups)), axis=1)
        else:
            fX = funct(y_channels_groups)
    return (fX - mean)/stdev

def calibration(y_channels_groups):
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
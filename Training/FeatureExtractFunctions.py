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

def getPeakCount(dchannel, w=3):
    ret = np.zeros((dchannel.shape[1], dchannel.shape[0]))
    for ch in range(dchannel.shape[0]):
        for sample in range(dchannel.shape[1]):
            count = 0
            for tind in range(w, dchannel.shape[2]-w):
                isPeak = True
                for x in range(1, w+1):
                    isPeak &= (dchannel[ch, sample, tind] > dchannel[ch, sample, tind-x] and dchannel[ch, sample, tind] > dchannel[ch, sample, tind+x])
                if(isPeak):
                    count+=1
            ret[sample, ch] = count
    return ret

def getPeakCount5(dchannel, w=5):
    ret = np.zeros((dchannel.shape[1], dchannel.shape[0]))
    for ch in range(dchannel.shape[0]):
        for sample in range(dchannel.shape[1]):
            count = 0
            for tind in range(w, dchannel.shape[2]-w):
                isPeak = True
                for x in range(1, w+1):
                    isPeak &= (dchannel[ch, sample, tind] > dchannel[ch, sample, tind-x] and dchannel[ch, sample, tind] > dchannel[ch, sample, tind+x])
                if(isPeak):
                    count+=1
            ret[sample, ch] = count
    return ret

def getPeakCount1(dchannel, w=1):
    ret = np.zeros((dchannel.shape[1], dchannel.shape[0]))
    for ch in range(dchannel.shape[0]):
        for sample in range(dchannel.shape[1]):
            count = 0
            for tind in range(w, dchannel.shape[2]-w):
                isPeak = True
                for x in range(1, w+1):
                    isPeak &= (dchannel[ch, sample, tind] > dchannel[ch, sample, tind-x] and dchannel[ch, sample, tind] > dchannel[ch, sample, tind+x])
                if(isPeak):
                    count+=1
            ret[sample, ch] = count
    return ret
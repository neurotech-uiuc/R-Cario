# In this file, I will train the example model with some fake data
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../Classifier/')
import Datacreate as dc
import spectogram_cnn as model

from PIL import Image
import matplotlib.pyplot as plt


path = "../../Recordings/Fall_2020/OpenBCISession_2020-10-11_16-26-10-YAN-RIGHT-FOOT/OpenBCI-RAW-2020-10-11_16-26-50.txt"
label_path = "../../Recordings/Labels/yanRightFoot"


def train():
    cnn = model.SpectogramCNN("modelFile")
    observations = dc.getObservationSet(path, label_path, 1000, [0,1,2], "R_FOOT")
    
    #do it for each channel
    # channel0 = observations[0]
    # generateTrainingData("SpectogramsData/YanLeftFoot/Channel0/", channel0)

    # channel1 = observations[1]
    # generateTrainingData("SpectogramsData/YanLeftFoot/Channel1/", channel1)

    # channel2 = observations[2]
    # generateTrainingData("SpectogramsData/YanLeftFoot/Channel2/", channel2)

    # and folder of stuff
    cnn.train((observations, ["SpectogramsData/YanLeftFoot/Channel0/", "SpectogramsData/YanLeftFoot/Channel1/", "SpectogramsData/YanLeftFoot/Channel2/"]))

def generateTrainingData(folderName, observations):
    # since they are all the same shape
    # x_data = observations[0][0]

    
    for i, y_data in enumerate(observations[0][1]):
        #generate and save spectogram
        fileName = '{}obs_{}'.format(folderName,i)
        genSpectogram(y_data, fileName)

def genSpectogram(y_data, fileName):
    # i took 200 from the Sample Rate = 200.0 Hz in datafile
    # plt.specgram(y_data, Fs=200)
    # plt.axis('off')
    # plt.savefig("./" + fileName + ".png", bbox_inches='tight', dpi=300, frameon='false')
    # plt.clf()

    fig,ax = plt.subplots(1)
    fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
    ax.axis('off')
    pxx, freqs, bins, im = ax.specgram(y_data, Fs=200)
    ax.axis('off')
    fig.savefig("./" + fileName + ".png", dpi=300, frameon='false', transparent=True, pad_inches=0.0 )
    fig.clf()
    plt.close()

#https://stackoverflow.com/questions/8598673/how-to-save-a-pylab-figure-into-in-memory-file-which-can-be-read-into-pil-image
# saves an image in memory
def fig2img(fig):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    import io
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)
    return img

def main():
    # print("Hello World!")
    train()

if __name__ == "__main__":
    main()


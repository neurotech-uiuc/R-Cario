# Pseudocode:

"""

    -- import the neccasary components -- 

    import Classifier as Classifier
    import RC_Controller as RC_Controller
    import RealTime_Capture as EEG

    model = Classifier.load(model="KNN")

    #if the below code takes longer than 500ms to run, 
    # either increase interval 
    # or make each iteration run in the background so it doesnt delay the next
    every 500ms: 
        # read stream should always return the same number of data points
        input = eeg.read_stream("1 second")
        outputLabel = model.classify(input)
        RC_Controller.sendSignal(outputLabel)


"""
import time
import datetime
import sys
import random
import beepy as beepy


outputLabels = []

def writeToFile(fileName):
    print("ATTEMPT WRITING TO FILE...")
    with open(fileName, 'w') as f:
        for item in outputLabels:
            f.write("%s\n" % item)
    print("WROTE TO FILE AND EXITED")

import sys, signal
def signal_handler(signal, frame):
    # print("\nprogram exiting gracefully")
    writeToFile()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main(argv):

    seconds = 120
    fileName = "recording.txt"

    # parse second
    if (argv[0] == "--sec"):
        seconds = int(argv[1])
        print("RECORDING FOR " + str(seconds) + " SECONDS")
    else:
        print("RECORDING FOR DEFAULT" + str(seconds) + " SECONDS")

    if (argv[2] == "--file"):
        fileName = argv[3]
        print("Saving at: " + fileName)
    

    start = datetime.datetime.now()

    while (datetime.datetime.now() - start).seconds < seconds:

        # print("Wait for prompt -- seconds elapsed:" , datetime.datetime.now() - start)
        secsToWaitBeforePromp = random.randint(5, 8)
        time.sleep(secsToWaitBeforePromp)
        beepy.beep(sound=1) # integer as argument
        print("PERFORM ACTION NOW -- elapsed:", datetime.datetime.now() - start)

        outputLabels.append(str(datetime.datetime.now().time()))
        time.sleep(3) #  wait 3 seconds to perform action


        
        
    writeToFile(fileName)

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        pass
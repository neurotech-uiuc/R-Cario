"""

Outputs random ones and zeros corresponding to actions for 60 seconds. (first 5 and last 5 are zero)

Should be done with data collection from external EEG software. 


"""

import time
import random
from datetime import datetime
arr = []
arr.append(0)
arr.append(0)
arr.append(0)
arr.append(0)
arr.append(0)
for i in range(60):
    val = random.randint(0, 1)
    arr.append(val)
arr.append(0)
arr.append(0)
arr.append(0)
arr.append(0)
arr.append(0)
start_time = datetime.now()
for i in range(60+5):
    print(str(arr[i]) + " " + str(arr[i+1]) + " " + str(arr[i+2]) + " " + str(arr[i+3]) + " " + str(arr[i+4]))
    time.sleep(1)
print(start_time)
print(arr)

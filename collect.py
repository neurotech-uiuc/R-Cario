import time
import random
from datetime import datetime

"""
Collect.py:

Generates an array of 70 1s and 0s corresponding to action and no action respectively.

First and last 5 numbers are 0, the rest are random.

Then, it iterates through it one second at a time, with the one corresponding to when the user should blink. 

User should start collecting using the external EEG software to collect data. 

Then, the start times should be lined up.

"""
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

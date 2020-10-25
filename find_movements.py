import csv
import numpy as np
import pandas as pd

def convert_timestamp(timestamp):
	return timestamp.replace(':', '').replace('\n', '')

def find_nearest(arr, val):
	idx = (np.abs(arr - val)).argmin()
	return idx, arr[idx]

# process raw data -----------------------------------------------------------------

num_channels = 3
num_header_lines = 6

data = [[] for i in range(num_channels + 1)]
print(data)

with open('Recordings/Fall_2020/OpenBCISession_2020-10-11_16-33-50-YAN-LEFT-EYE/OpenBCI-RAW-2020-10-11_16-38-59.txt', 'r') as data_csv:
	csvreader = csv.reader(data_csv, delimiter=',')

	# skip header lines
	for i in range(num_header_lines):
		next(csvreader, None)

	for row in csvreader:
		# print(row[8])
		data[0].append(float(convert_timestamp(row[8])))
		for i in range(1, 1 + num_channels):
			data[i].append(float(row[i]))

# print(data)
data = np.array(data)
# print(data)
# print(times)

args = np.argsort(data[0])
for i in range(data.shape[0]):
	data[i] = data[i][args]
print(data)

times = data[0]

# process timestamps -----------------------------------------------------------------

move_times = None
with open('Recordings/Labels/yanLeftEye') as timestamps:
	move_times = np.array([convert_timestamp(row) for row in timestamps])
print(move_times)


# -----------------------------------------------------------------

move_interval = 1
channel_avgs = [[] for i in range(num_channels)]

for move_time in move_times:
	idx, nearest_val = find_nearest(times, move_time)
	channels_vals = [[] for i in range(num_channels)]

	while (times[idx] < nearest_val + move_interval):
		for i in range(1, 1 + num_channels):
			channel_vals[i - 1].append(data[i][idx])
		idx += 1

	channel_vals = np.array(channel_vals)
	for i in range(channel_vals.shape[0]):
		channel_avgs[i].append(np.mean(channel_vals[i]))

channel_avgs = np.array(channel_avgs)
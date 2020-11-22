import argparse
import time
import numpy as np

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations


class Capture():
    # boardID = 1 for ganglion
    # serialPort : https://brainflow.readthedocs.io/en/stable/SupportedBoards.html#ganglion
    def __init__(self, boardID, serial_port):
        self.serial_port = serial_port
        params = BrainFlowInputParams()
        params.serial_port = serial_port
        BoardShim.disable_board_logger ()
        self.board = BoardShim (boardID, params)
        self.board.prepare_session()

    def startStream(self):
        self.board.start_stream()
        
    # so given this many seconds it will try to get num_samples of data
    # if seconds is too small, num_samples returned won't be enough
    def getData(self, num_seconds, num_samples):
        time.sleep(num_seconds)
        # data = self.board.get_current_board_data (num_samples)
        data = self.board.get_board_data()[:190]
        
        # gets 0,1,2 channel. ignore 4 b/c noise data
        return np.array([data[1], data[2], data[3]])

    def closeStream(self):
        self.board.stop_stream()
        self.board.release_session()

# def main ():
#     parser = argparse.ArgumentParser ()
#     # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
#     parser.add_argument ('--timeout', type = int, help  = 'timeout for device discovery or connection', required = False, default = 0)
#     parser.add_argument ('--ip-port', type = int, help  = 'ip port', required = False, default = 0)
#     parser.add_argument ('--ip-protocol', type = int, help  = 'ip protocol, check IpProtocolType enum', required = False, default = 0)
#     parser.add_argument ('--ip-address', type = str, help  = 'ip address', required = False, default = '')
#     parser.add_argument ('--serial-port', type = str, help  = 'serial port', required = False, default = '')
#     parser.add_argument ('--mac-address', type = str, help  = 'mac address', required = False, default = '')
#     parser.add_argument ('--other-info', type = str, help  = 'other info', required = False, default = '')
#     parser.add_argument ('--streamer-params', type = str, help  = 'streamer params', required = False, default = '')
#     parser.add_argument ('--serial-number', type = str, help  = 'serial number', required = False, default = '')
#     parser.add_argument ('--board-id', type = int, help  = 'board id, check docs to get a list of supported boards', required = True)
#     parser.add_argument ('--file', type = str, help  = 'file', required = False, default = '')
#     parser.add_argument ('--log', action = 'store_true')
#     args = parser.parse_args ()

    # params = BrainFlowInputParams ()
    # params.ip_port = args.ip_port
    # params.serial_port = args.serial_port
    # params.mac_address = args.mac_address
    # params.other_info = args.other_info
    # params.serial_number = args.serial_number
    # params.ip_address = args.ip_address
    # params.ip_protocol = args.ip_protocol
    # params.timeout = args.timeout
    # params.file = args.file

#     if (args.log):
#         BoardShim.enable_dev_board_logger ()
#     else:
#         BoardShim.disable_board_logger ()

#     board = BoardShim (args.board_id, params)
#     board.prepare_session ()

#     # board.start_stream () # use this for default options
#     board.start_stream ()
#     time.sleep (1)

#     time_channel = board.get_timestamp_channel (args.board_id) 

#     data = board.get_current_board_data (190) # get latest 256 packages or less, doesnt remove them from internal buffer
#     # data = board.get_board_data () # get all data and remove it from internal buffer
#     board.stop_stream ()
#     board.release_session ()

#     # print(board.get_board_data_count())
#     # print(board.get_eeg_channels(args.board_id))

#     # print (len(data[0]))
#     # print(data)
#     # print(data[0])
#     # for e in data[0:1]:
#     #     print(*e, sep = "") 
#     print(len(data[0]))
#     print(len(data[1]))
#     # print(data[1])
#     # print(data[2])   

#     # print(data[time_channel])

#     print(data[1][0:10])


# # python Capture.py --board-id 1 --serial-port /dev/cu.usbmodem11
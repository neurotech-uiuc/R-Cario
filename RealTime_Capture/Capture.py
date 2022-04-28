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
        
        # gets 0,1,2,3 channel
        return np.array([data[1], data[2], data[3], data[4]])

    def closeStream(self):
        self.board.stop_stream()
        self.board.release_session()

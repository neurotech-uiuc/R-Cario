import bluetooth
import serial
import time
import numpy as np
class Controller():
	def __init__(self, serial_speed, serial_port):
		self.serial_speed = serial_speed
		self.serial_port = serial_port
	
	def connect(self):
		self.ser = serial.Serial(self.serial_port, self.serial_speed, timeout=1)

	def close(self):
		self.ser.close()


	def sendAction(self, action):
		actionInt = np.argmax(action)
		actionLabel = "S"
		if actionInt == 3: # L_EYE
			actionLabel = "U"
		elif actionInt == 4: # R_EYE
			actionLabel = "D"
		
		self.ser.write(bytes(actionLabel, 'utf-8'))
		print("recieving message from arduino ...")
		res = self.ser.readline()
		if (res != ""):
			print("arduino says: %s" % res)
		else:
			print("arduino doesnt respond")

		time.sleep(.5)

		# STOP THE ACTION 
		self.ser.write(b'S')
		print("recieving message from arduino ...")
		res = self.ser.readline()
		if (res != ""):
			print("arduino says: %s" % res)
		else:
			print("arduino doesnt respond")
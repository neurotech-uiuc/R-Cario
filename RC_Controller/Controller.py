import bluetooth
import serial
import time
import numpy as np


"""
	Controller Class for Arduino hardware
	Receives serial port that Arduino bluetooth is connected to
	Tracks moving time to prevent unwanted behavior after an arbitrary amount of time
	Receives an array of values from a classifier and processes based on the action with highest likelihood of occurrence
	Actions include: L_EYE, R_EYE, JAW_CLENCH, EYEBROW_RAISE, EYEBROW_DOWN
"""
class Controller():
	def __init__(self, serial_speed, serial_port):
		self.serial_speed = serial_speed
		self.serial_port = serial_port
		self.moving = False
		self.turning = False
		self.moving_time = 0
		self.MAX_MOVE_TIME = 10


	def connect(self):
		self.ser = serial.Serial(self.serial_port, self.serial_speed, timeout=1)
		if(not self.ser.isOpen()):
			print("opening port")
			self.ser.open()
		else:
			print("Already opened")


	def close(self):
		self.ser.close()


	"""
		sendAction processes the action and writes a stream to the port to be received by the Arduino
		actionLabel is a single character keeps track of what action that is determined:
			"S": no action/stop action
			"L": turn left
			"R": turn right
			"U": start/stop moving
			"H": increase speed
			"G": decrease speed
		New actions can be added by appending to the conditionals below 
		A new character should be allocated for every new action appended
	"""
	def sendAction(self, action):
		actionInt = np.argmax(action)
		actionLabel = "S"
		if actionInt == 1: # L_EYE
			self.sendStopAction()
			self.moving_time = 0
			actionLabel = "L"
			self.turning = True

		elif actionInt == 2: # R_EYE
			self.sendStopAction()
			self.moving_time = 0
			actionLabel = "R"
			self.turning = True

		elif actionInt == 3: # JAW_CLENCH
			if (self.moving):
				actionLabel = "S"
				self.moving = False
				self.moving_time = 0
			else:
				actionLabel = "U" 
				self.moving = True
				self.moving_time += 1

		elif actionInt == 4: # EYEBROW_RAISE
			if (self.moving):
				self.sendStopAction()
				self.moving = False
				self.moving_time = 0
			actionLabel = "H"

		elif actionInt == 5: # EYEBROW_DOWN
			if (self.moving):
				self.sendStopAction()
				self.moving = False
				self.moving_time = 0
			actionLabel = "G"
		
		# keeps car moving if not prompted to stop
		if (self.moving and actionLabel == "S"):
			if (self.moving_time > self.MAX_MOVE_TIME):
				self.sendStopAction()
				self.moving = False
				self.moving_time = 0
			else:
				self.moving_time += 1
			return

		print("Sending %s" % actionLabel)
		self.ser.write(bytes(actionLabel, 'utf-8'))
		print("receiving message from arduino ...")
		res = self.ser.readline()
		if (res != ""):
			print("arduino says: %s" % res)
		else:
			print("arduino doesnt respond")

		if (self.turning):
			time.sleep(0.5)
			self.sendStopAction()
			self.turning = False
		
		if (self.moving):
			time.sleep(0.1)

	"""
		Helper function to stop the current action when necessary throughout sendAction
	"""
	def sendStopAction(self):
		self.ser.write(b'S')
		print("recieving message from arduino ...")
		res = self.ser.readline()
		if (res != ""):
			print("arduino says: %s" % res)
		else:
			print("arduino doesnt respond")


	def getSer(self):
		return self.ser

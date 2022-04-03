import bluetooth
import serial
import time
import numpy as np
class Controller():
	def __init__(self, serial_speed, serial_port):
		self.serial_speed = serial_speed
		self.serial_port = serial_port
		self.moving_forward = False
		self.moving_backward = False
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


	def sendAction(self, action):
		actionInt = np.argmax(action)
		actionLabel = "S"
		if actionInt == 1: # L_EYE
			self.sendStopAction()
			self.moving_time = 0
			actionLabel = "R"
			self.turning = True
		elif actionInt == 2: # R_EYE
			self.sendStopAction()
			self.moving_time = 0
			actionLabel = "L"
			self.turning = True

		elif actionInt == 3: # JAW_CLENCH
			if (self.moving_backward):
				self.sendStopAction()
			if (self.moving_forward):
				actionLabel = "S"
				self.moving_forward = False
				self.moving_time = 0
			else:
				actionLabel = "U" 
				self.moving_forward = True
				self.moving_time += 1

		elif actionInt == 4: # EYEBROW_RAISE
			if (self.moving_forward):
				self.sendStopAction()
			if (self.moving_backward):
				actionLabel = "S"
				self.moving_backward = False
				self.moving_time = 0
			else:
				actionLabel = "D"
				self.moving_backward = True
				self.moving_time += 1

		# keeps car moving if no action is presented
		if (self.moving_forward or self.moving_backward and actionLabel == "S"):
			if (self.moving_time > self.MAX_MOVE_TIME):
				self.sendStopAction()
				self.moving_backward = False
				self.moving_forward = False
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

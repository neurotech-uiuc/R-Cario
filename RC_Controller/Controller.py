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


# import bluetooth

# serverMACAddress = '98:D3:31:F7:7B:E5'
# port = 1
# s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
# s.connect((serverMACAddress, port))
# while 1:
#     text = input() # Note change to the old (Python 2) raw_input
#     if text == "quit":
#     	break
#     s.send('D')
# s.close()

# import serial
# import time

# # # Serial port parameters
# serial_speed = 9600
# serial_port = '/dev/cu.HC-06-SPPDev' # bluetooth shield hc-06


# if __name__ == '__main__':
# 	print("conecting to serial port ...")
# 	ser = serial.Serial(serial_port, serial_speed, timeout=1)
# 	while(1):
# 		text = input("INPUT: ")
# 		if text == "exit":
# 			break
# 		print("sending message...")
# 		# ser.write(bytes(b'L'))
# 		ser.write(bytes(text, 'utf-8'))

# 		print("recieving message from arduino ...")
# 		data = ser.readline()

# 		if (data != ""):
# 			print("arduino says: %s" % data)
# 		else:
# 			print("arduino doesnt respond")

# 	print("finish program and close connection!")
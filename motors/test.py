# import motors
# from motors import movement as move
import serial

import time
from serial import Serial

# Open serial port

FILTER = 15
# counter = 0
ser = serial.Serial()
ser.port = 'COM4'  # Port 485 for motor
ser.baudrate = 9600
ser.timeout = 0.01
ser.setDTR(False)
ser.open()
ser.write(b"OFF")
ser.close()
#############################################################
rx = bytes(0)
i = 0
# channel = []


# while True:
#     # command = str('ON')
#     ser.write(b'ON')

# if command == 'exit':
#     exit()

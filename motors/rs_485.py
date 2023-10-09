# import motors
# from motors import movement as move
import serial

import time
from serial import Serial

# Open serial port

FILTER = 15
# counter = 0
ser = serial.Serial()
ser.port = '/dev/ERBoard'  # Port 485 for motor
# ser.port = '/dev/ttyUSB1'
ser.baudrate = 115200
ser.timeout = 0.1
ser.setDTR(False)
ser.open()
#############################################################
rx = bytes(0)
i = 0
# channel = []


def read_from_port(ss):

    while True:
        # global note1
        # print("NO")
        # print(ss.in_waiting)
        while ss.in_waiting > 0:
            
            # global rx
            # checkChannel = 1
            # print(ss.readline())
            # rx = ss.readline().decode(encoding='ascii', errors='ignore').rstrip('\r\n')
            # ss.flushInput()
            # print(rx)
            # channel = rx.rstrip(',').split(',')
            # for i in range(0, 12):
            #     # print(i)
            #     if (len(channel) == 16):
            #         if (channel[i] == ''):
            #             checkChannel = 0
            #             break
            #         elif (int(channel[0]) < 282):
            #             channel[0] = '1002'
            #             checkChannel = 1
            #         else:
            #             checkChannel = 1
            #     else:
            #         checkChannel = 0
            #         break
            #     # print(checkChannel)
            #     # print(channel[1])
            # if (checkChannel == 1):
            #     # print(channel)
            #     return channel
            
            try :
                global arrx 
                arrx = ss.read(100)
                ss.flushInput()
                txt = str(arrx, 'UTF-8')
                # print(txt)
                channel = txt.rstrip(',').split(',')
                print(channel)
                # for i in range(0,12):
                #     print(channel[i])
                return channel
            except serial.serialutil.SerialException :
                continue
            
            


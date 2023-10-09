# import motor_handlers as motor
# from motors import movement as move
import serial

import time
from serial import Serial

# Open serial port

FILTER = 15
# counter = 0
ser = serial.Serial()
ser.port = '/dev/USBCan'  # Port 485 for motor
# ser.port = '/dev/ttyUSB2'
ser.baudrate = 115200
ser.timeout = 0.01
ser.setDTR(False)
ser.open()
#############################################################
rx = bytes(0)
i = 0
# channel = []
# data = [170, 200, 71, 1, 162, 0, 0, 0, 192, 198, 45, 0, 85]

# while True:
#     ser.write(data)

# def read_from_port(ss):
#     while True:
#         if ser.in_waiting > 0:
#             global rx
#             # global counter
#             rx = ss.read(100)
#             # data = ss.readline().decode().rstrip('\r\n')
#             # value = ser.readline().decode('utf-8').rstrip('\r\n')
#             # ss.flushInput()
#             # if value:
#             #     print(value)\
#             # counter = 0
#             # while counter < 16:
#             # while True:
#             #     value = ser.readline().decode(encoding='ascii', errors='ignore').rstrip('\r\n')
#             #     if value:
#             #         data = value.split(',')
#             #         channel.append(data[:15])
#             #     print(channel)
#         value = ser.readline().decode(encoding='ascii', errors='ignore').rstrip('\r\n')
#         if value
#         # test = int(value)
#         # print("test", x, ":", test)
#         # print("val: ", value)
#         # if value:
#         #     num = int(value)
#         #     print("val: ", value)
#         #     channel.append(num)
#         #     print(counter, ":", channel[counter])
#         #     counter = counter + 1
#             # channel.append(num)  # add data to array
#         # value = ser.readline().decode(encoding='utf-8', errors='ignore').rstrip('\n')
#             # num = int(value)
#             # print(num)
#         # if i % 14 == 0:
#         #     i = 0
#         # print(i, ":", num)
#         # i = i + 1
#         # output_string = str(rx, 'utf-8')
#         # print(output_string)


def read_from_port(ss):
    while True:
        global note1
        while ss.in_waiting > 0:
            global rx

            rx = ss.read(100)
            # data = ser.readline().decode().rstrip('\r\n')
            ss.flushInput()
            # output_string = str(rx, 'utf-8')
            # print(output_string.rstrip(',').split(','))
            # channel = output_string.rstrip(',').split(',')
            # if channel:
            #     return channel
            # time.sleep(1)
            # print(channel)
            # return channel

        # num = int(output_string)
        # data_array.append(num[:16])

        # print(data)
        # if data:
        #     data_array.append(data) # add data to array
        #     print(data_array) # 
        # print array contents (optional)
        # return channel

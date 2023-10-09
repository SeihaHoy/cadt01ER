import time
import motors.can as com
# import motors.rs_485_port as rs485_com
# import motors.rs_485 as com
import log_msg.logger as log
from bitstring import BitArray

header = [0xaa, 0xc8]   # The CAN message inside stays the same
trailer = [0x55] 
# def int_byte(int_data):
#     return (int_data & 0xff)

# def ratio(idm, ang, velo):
#     """TODO ask about ratio of motor 1 and 2"""
#     if idm == 1:
#         ang *= 4.5
#         velo *= 4.5
#     elif idm == 2:
#         ang *= 240
#         velo *= 1.0
#     else:
#         ang *= -1.0
#     return int(ang*100), int(velo*100)


# def trans(data):
#     com.ser.flushOutput()
#     com.ser.write(data)
#     while True:
#         print("wait in loop")
#         time.sleep(5)
#         if(len(com.rx)>0):
#             if((com.rx[0] == data[0]) and (com.rx[1] == data[1]) and (com.rx[2] == data[2])):
#                 break
#     time.sleep(0.01)

# def reset_error(idm):
#     motor=[]
#     motor.append(0x3e)
#     motor.append(0x9b)
#     motor.append(idm)
#     motor.append(0x00)
#     motor.append(int_byte(motor[0]+motor[1]+motor[2]+motor[3]))

# def stopmotor(idm):
#     mstop = []
#     mstop.append(0x3e)
#     mstop.append(0x80)
#     mstop.append(idm)
#     mstop.append(0x00)
#     mstop.append(int_byte(mstop[0]+mstop[1]+mstop[2]+mstop[3]))
#     trans(mstop)

# def runmotorspeed(idm, angle, velocity):
#     chsum =0
#     degree,speed = ratio(idm, angle, velocity)
#     move_motor = []
#     move_motor.append(0x3e)
#     move_motor.append(0xa8)
#     move_motor.append(idm)
#     move_motor.append(0x08)
#     move_motor.append(int_byte(move_motor[0]+move_motor[1]+move_motor[2]+move_motor[3]))
#     for i in range(5,13):
#         if i in range(5,9):
#             move_motor.append(int_byte(degree >> 8*(i-5)))
#         if i in range(9,13):
#             move_motor.append(int_byte(speed >> 8*(i-9)))
#         chsum += move_motor[i]
#     move_motor.append(int_byte(chsum))
#     trans(move_motor)

# def readangle(idm):
#     _result=0
#     motor_data = []
#     motor_data.append(0x3e)
#     motor_data.append(0x92)
#     motor_data.append(idm)
#     motor_data.append(0x00)
#     motor_data.append(int_byte(motor_data[0]+motor_data[1]+motor_data[2]+motor_data[3]))
#     trans(motor_data)
#     if((com.rx[0] == 0x3e) and (com.rx[1] == 0x92) and (com.rx[2] == idm)):
#         for i in range(5,13):
#             _result |= com.rx[i] << (8*(i-5))
#     s = "{:016b}".format(_result & 0xffffffff)
#     _resulttemp = BitArray(bin=s).int
#     result = _resulttemp / 100.0

#     if(idm == 1):
#         result /= 4.5
#     elif(idm == 2):
#         result /= 240
#     else:
#         result *= -1.0
#     print(idm, "[Angle]", result)
#     return  result
global pre_angle
pre_angle = 0.0


def int_byte(int_data):
    return (int_data & 0xff)


def ratio(mid, ang, velo):
    if mid == 1:
        ang *= 6.0
        velo *= 6.0
    elif mid == 2:
        ang *= 6.0
        velo *= 6.0
    elif mid == 3:
        ang *= 6.0
        velo *= 6.0
    elif mid == 4:
        ang *= 6.0
        velo *= 6.0
    elif mid == 5:
        ang *= 9.0
        velo *= 9.0
    elif mid == 6:
        ang *= 9.0
        velo *= 9.0
    else:
        ang *= 30.0
        velo *= 30.0
    return int(ang*100), int(velo*100)


def trans(data):
    try:
        if not com.ser.is_open:
            pass
            print("Interface: " + str(com.ser.is_open))
        else:
            com.ser.reset_output_buffer()
            com.ser.write(data)
    except Exception as error:
        com.ser.close()
        print(error)

    # while (True):
    #     # print("wait")
    #     if (len(com.rx) > 0):
    #         # print("Hello5")
    #         if ((com.rx[0] == data[0])):
    #             break
    # time.sleep(0.1)

    # def write(data):
    # try:
    #     if not interface.is_open:
    #         pass
    #         print("Interface: " + str(interface.is_open))
    #     else:
    #         interface.reset_output_buffer()
    #         interface.write(data)
    # except Exception as error:
    #     interface.close()
    #     print(error)

def trans_rs485(data):
    rs485_com.ser.flushOutput()
    rs485_com.ser.write(data)
    print(data)

    while (True):
        # print("wait")
        if(com.rx != None):

            if (len(com.rx) > 0):
                # print("Hello5")
                if ((com.rx[0] == data[0])):
                    break
        else :
            print("null")
            continue
        
    # time.sleep(0.1)


def reset_error(mid):
    m_data = []
    m_data.append(0x3e)
    m_data.append(0x9b)
    m_data.append(mid)
    m_data.append(0x00)
    m_data.append(int_byte(m_data[0] + m_data[1] + m_data[2] + m_data[3]))
    trans_rs485(m_data)


def stopmotor(mid):
    m_data = []
    m_data.append(0x3e)
    m_data.append(0x81)
    m_data.append(mid)
    m_data.append(0x00)
    m_data.append(int_byte(m_data[0] + m_data[1] + m_data[2] + m_data[3]))
    trans_rs485(m_data)


def stopmotor1(mid):
    m_data = []
    m_data.append(0xaa)
    m_data.append(0xc8)
    m_data.append(0x40+mid)
    m_data.append(0x01)
    # m_data.append(0x80)
    # m_data.append(0x02)
    m_data.append(0x81)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x55)
    trans(m_data)


def runInc_speed_rs485(mid, ang, velo):
    chsum = 0
    degree, speed = ratio(mid, ang, velo)
    m_data = []
    m_data.append(0x3e)
    m_data.append(0xa8)
    m_data.append(mid)
    m_data.append(0x08)
    m_data.append(int_byte(m_data[0] + m_data[1] + m_data[2] + m_data[3]))
    for i in range(5, 13):
        if i in range(5, 9):
            m_data.append(int_byte(degree >> 8*(i-5)))
        if i in range(9, 13):
            m_data.append(int_byte(speed >> 8 * (i - 9)))
        chsum += m_data[i]
    m_data.append(int_byte(chsum))
    trans_rs485(m_data)

def runMulti_Angle_speed_rs_485(mid,ang,velo):
    chsum = 0
    degree,speed = ratio(mid,ang,velo)
    if(speed == 0):
        speed = 1
    m_data = []
    m_data.append(0x3e)
    m_data.append(0xa4)
    m_data.append(mid)
    m_data.append(0x0c)
    m_data.append(int_byte(m_data[0] + m_data[1] + m_data[2] + m_data[3]))
    for i in range(5,17):
        if i in range(5,13):
            m_data.append(int_byte(degree >> 8*(i-5)))
        if i in range(13,17):
            m_data.append(int_byte(speed >> 8 * (i - 13)))
        chsum += m_data[i]
    m_data.append(int_byte(chsum))
    trans_rs485(m_data)


def runMulti_Angle_speed(mid, ang, velo):
    chsum = 0
    degree, speed = ratio(mid, ang, velo)
    if (speed == 0):
        speed = 1
    m_data = []
    m_data.append(0xaa)
    m_data.append(0xc8)
    m_data.append(0x40+mid)
    m_data.append(0x01)
    m_data.append(0xa4)
    m_data.append(0x00)
    # m_data.append(0xf4)
    # m_data.append(0x01)
    for i in range(8, 10):
        m_data.append(int_byte(speed >> 8 * (i - 8)))
    for i in range(10, 14):
        m_data.append(int_byte(degree >> 8 * (i - 10)))
    m_data.append(0x55)
    print(m_data)
    trans(m_data)

# def incre_position(mid, speed, angle):
#     chsum = 0
#     m_data = []
#     m_data.append(0x3e)
#     m_data.append(0x00+mid)
#     m_data.append(0x08)
#     m_data.append(0xa8)
#     m_data.append(0x00)
#     for i in range (6, 12):
#         if i in range (6,8):
#             m_data.append(int_byte(speed >> 8 * (i - 6)))
#         if i in range(8, 12):
#             m_data.append(int_byte(angle >> 8 * (i - 8)))
#     for i in range(0, 11):
#         chsum += m_data[i]
#     m_data.append(int_byte(chsum))
#     m_data.append(int_byte(chsum >> 8))
#     print(m_data)
#     trans_rs485(m_data)

# def runInc_speed_can(mid, ang, velo):
#     degree, speed = ratio(mid, ang, velo)
#     m_data = []
#     m_data.append(0xaa)
#     m_data.append(0xc8)
#     m_data.append(0x40+mid)
#     m_data.append(0x01)
#     m_data.append(0xa8)
#     m_data.append(0x00)
#     for i in range (6, 12):
#         if i in range (6,8):
#             m_data.append(int_byte(speed >> 8 * (i - 6)))
#         if i in range(8, 12):
#             m_data.append(int_byte(degree >> 8 * (i - 8)))
#     m_data.append(0x55)
#     trans(m_data)

def runInc_speed(mid, velo, ang):
    chsum = 0
    degree, speed = ratio(mid, velo, ang)
    m_data = []
    m_data.append(0xaa)
    m_data.append(0xc8)
    m_data.append(0x40+mid)
    m_data.append(0x01)
    m_data.append(0xa8)
    m_data.append(0x00)
    # for i in range(6, 13):
    #     if i in range(6, 8):
    #         m_data.append(int_byte(degree >> 8*(i-6)))
    #     if i in range(8, 12):
    #         m_data.append(int_byte(speed >> 8 * (i - 8)))
    for i in range(6, 13):
        if i in range(6, 8):
            m_data.append(int_byte(speed >> 8*(i-6)))
        if i in range(8, 12):
            m_data.append(int_byte(degree >> 8 * (i - 8)))
    m_data.append(0x55)
    trans(m_data)
    # speed *= 0.01
    # degree, speed = ratio(mid, ang, velo)
    # data = header + [0x40 + mid, 0x01, 0xa8, 0x00]
    # for i in range(0, 2):
    #     data.append((speed >> 8 * i) & 0xff)
    # for j in range(0, 4):
    #     data.append((degree >> 8 * j) & 0xff)
    # data += trailer
    # trans(data)

def run_speed(mid, velo):
    # chsum = 0
    degree, speed = ratio(mid, 0, velo)
    # if(speed == 0):
    #     speed = 1
    # if(speed > 72000):
    #     speed = 72000
    # if (speed < -72000):
    #     speed = -72000
    m_data = []
    m_data.append(0xaa)
    m_data.append(0xc8)
    m_data.append(0x40+mid)
    m_data.append(0x01)
    m_data.append(0xa2)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    for i in range(8, 12):
        m_data.append(int_byte(speed >> 8 * (i - 8)))
    m_data.append(0x55)
    # print(m_data)
    trans(m_data)


def readAngle(mid):
    global pre_angle
    _result = 0
    result = 0
    m_data = []
    m_data.append(0x3e)
    m_data.append(0x92)
    m_data.append(mid)
    m_data.append(0x00)
    m_data.append(int_byte(m_data[0] + m_data[1] + m_data[2] + m_data[3]))
    trans_rs485(m_data)
    if (len(com.rx) >= 14):
        if ((com.rx[0] == 0x3e) and (com.rx[1] == 0x92) and (com.rx[2] == mid)):
            for i in range(5, 13):
                _result |= com.rx[i] << (8*(i-5))
        s = "{:016b}".format(_result & 0xffffffff)
        _resulttemp = BitArray(bin=s).int
        # print(_resulttemp)
        result = _resulttemp / 100.0
        if (mid == 1):
            result /= 9.0
        elif (mid == 2):
            result /= 9.0
        elif (mid == 3):
            result /= 9.0
        else:
            result /= 30.0
        pre_angle = result
        return result
    else:
        return pre_angle

def readAngle_can(mid):
    global pre_angle
    _result = 0
    result = 0
    m_data = []
    m_data.append(0xaa)
    m_data.append(0xc8)
    m_data.append(0x40+mid)
    m_data.append(0x01)
    m_data.append(0x92)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x55)
    trans(m_data)
    if (len(com.rx) >= 14):
        if ((com.rx[0] == 0xaa) and (com.rx[1] == 0xc8) and (com.rx[2] == 0x40+mid)):
            for i in range(5, 13):
                _result |= com.rx[i] << (8*(i-5))
        s = "{:016b}".format(_result & 0xffffffff)
        _resulttemp = BitArray(bin=s).int
        # print(_resulttemp)
        result = _resulttemp / 100.0
        if (mid == 1):
            result /= 9.0
        elif (mid == 2):
            result /= 9.0
        elif (mid == 3):
            result /= 9.0
        else:
            result /= 30.0
        pre_angle = result
        return result
    else:
        return pre_angle

def readSpeed(mid):
    result = 0
    m_data = []
    m_data.append(0x3e)
    m_data.append(0x9c)
    m_data.append(mid)
    m_data.append(0x00)
    m_data.append(int_byte(m_data[0] + m_data[1] + m_data[2] + m_data[3]))
    trans_rs485(m_data)
    while (len(com.rx) == 0):
        if ((com.rx[0] == 0x3e) and (com.rx[1] == 0x9c) and (com.rx[2] == mid)):
            result = (com.rx[9] << 8) | (com.rx[8])
            if (mid == 1):
                result /= 9.0
            elif (mid == 2):
                result /= 9.0
            elif (mid == 3):
                result /= 9.0
    return result

def readSpeed_can(mid):
    result = 0
    m_data = []
    m_data.append(0xaa)
    m_data.append(0xc8)
    m_data.append(0x40+mid)
    m_data.append(0x01)
    m_data.append(0x9c)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x55)
    trans(m_data)
    while (len(com.rx) == 0):
        if ((com.rx[0] == 0xaa) and (com.rx[1] == 0xc8) and (com.rx[2] == 0x40+mid)):
            result = (com.rx[9] << 8) | (com.rx[8])
            if (mid == 1):
                result /= 9.0
            elif (mid == 2):
                result /= 9.0
            elif (mid == 3):
                result /= 9.0
    return result


def readEncoder(mid):
    result = 0
    m_data = []
    m_data.append(0x3e)
    m_data.append(0x90)
    m_data.append(mid)
    m_data.append(0x00)
    m_data.append(int_byte(m_data[0] + m_data[1] + m_data[2] + m_data[3]))
    trans_rs485(m_data)
    while (len(com.rx) == 0):
        print('wait')
        if ((com.rx[0] == 0x3e) and (com.rx[1] == 0x90) and (com.rx[2] == mid)):
            result = (com.rx[9] << 8) | (com.rx[8])
    return result


def readEncoder_can(mid):
    result = 0
    m_data = []
    m_data.append(0xaa)
    m_data.append(0xc8)
    m_data.append(0x40+mid)
    m_data.append(0x01)
    m_data.append(0x90)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x00)
    m_data.append(0x55)
    trans(m_data)
    while (len(com.rx) == 0):
        print('wait')
        if ((com.rx[0] == 0xaa) and (com.rx[1] == 0xc8) and (com.rx[2] == 0x40+mid)):
            result = (com.rx[9] << 8) | (com.rx[8])
    return result


def writeM0(mid):
    readEncoder(mid)
    m_data = []
    m_data.append(0x3e)
    m_data.append(0x91)
    m_data.append(mid)
    m_data.append(0x02)
    m_data.append(int_byte(m_data[0] + m_data[1] + m_data[2] + m_data[3]))
    m_data.append(com.rx[7])
    m_data.append(com.rx[8])
    m_data.append(int_byte(m_data[5] + m_data[6]))
    trans(m_data)
    stopmotor1(mid)
    runInc_speed(mid, 0.01, 50)

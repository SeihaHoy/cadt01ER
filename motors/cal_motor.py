import motors.motor_handlers as mm
import time

def move_motor():
    # mm.runmotorspeed(1, -1, 1800)
    # time.sleep(5)
    # mm.runmotorspeed(2, -30, 3600)
    mm.readangle(1)
    mm.readangle(2)

# def setzero():


# def findtarget():

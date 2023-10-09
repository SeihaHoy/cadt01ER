import log_msg.logger as log
import motors.cal_motor as mm
import threading
import motors.motor_handlers as motor
# import motors.monent as mo
# import cv2
# new
import time
import motors.rs_485 as com
import motors.can as can
# import motors.rs_485_port as rs485
# import test_distance.tracking as pos
global reload

# from obj_detection ie-packages/serial/serialposix.py", line 325, in open
    # raise SerialException(msg.errno, "could nomport get_frame, release

# def obj_detect():
#     while True:
#         (detected, img, color_data) = get_frame()
#         # if len(detected) > 0:
#         # Write latest results into file
#         # f = open('__detected.txt', 'wb')
#         # pickle.dump(detected, f)
#         # f.write(pickle.dumps(detected).decode("utf-8"))
#         # f.close()
#         # 0 for waiting key pressed, 1 for waiting every 1ms
#         key = cv2.waitKey(1)
#         if key == 27:  # Esc key
#             # Write latest result into file
#             log.info("Write data to __detected.txt")
#             f = open('__detected.txt', 'w')
#             f.write(json.dumps(detected))
#             f.close()

#             log.info("Write image to __detected_img.png")
#             # cv2.imwrite('__detected_img1.png', img)

#             cv2.destroyAllWindows()
#             release()
#             break


def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


def mainprog():
    global reload
    while True:
        # print("hi")
        controller = com.read_from_port(com.ser,)
        print(len(controller))
        print(int(controller[2]))
        # if (len(controller) == 17):
        #     if(int(controller[6])==1722) : #backward_pickup
        #         if(reload == 1):
        #             motor.runInc_speed(1,-370 ,100) #4225  4225
        #             motor.runInc_speed(2,370 ,100)
        #             motor.runInc_speed(3,-370 ,100)
        #             motor.runInc_speed(4,370 ,100)
        #             # time.sleep(0.462)
        #             time.sleep(0.53)
        #             com.ser.write("Pickup".encode())
                    
        #             reload = 0
        #     elif(int(controller[6])==282):
        #             # motor.run_speed(1, 0)
        #             # motor.run_speed(2, 0)
        #             # motor.run_speed(3, 0)
        #             # motor.run_speed(4, 0)
        #         reload = 1

        if (len(controller) == 17):
            offset = int(controller[10])
            # reload = 1
            # motor.run_speed(1,100)
        #     print(controller)
            # for i in range(0,17):
            #     print(controller[i])
        
            if (int(controller[5]) == 1722):
                            
               
                if (int(controller[2]) > 1004):  # Forward
                    duty_cycle = map_range(
                        int(controller[2]), 1004, 1722, 0, 500)
                    if (int(controller[3]) > 1004):
                        motor.run_speed(1, 1*duty_cycle)
                        motor.run_speed(2, 0*duty_cycle)
                        motor.run_speed(3, 0*duty_cycle)
                        motor.run_speed(4, -1*duty_cycle)
                    elif (int(controller[3]) < 1000):
                        motor.run_speed(1, 0*duty_cycle)
                        motor.run_speed(2, -1*duty_cycle)
                        motor.run_speed(3, 1*duty_cycle)
                        motor.run_speed(4, 0*duty_cycle)
                    else:
                        motor.run_speed(1, 1*duty_cycle)
                        motor.run_speed(2, -1*duty_cycle)
                        motor.run_speed(3, 1*duty_cycle)
                        motor.run_speed(4, -1*duty_cycle)
                elif (int(controller[2]) < 1000):  # Backward
                    
                    duty_cycle = map_range(
                        int(controller[2]), 1000, 282, 0, 400)
                    if (int(controller[3]) > 1004):
                        motor.run_speed(1, 0*duty_cycle)
                        motor.run_speed(2, 1*duty_cycle)
                        motor.run_speed(3, -1*duty_cycle)
                        motor.run_speed(4, 0*duty_cycle)
                    elif (int(controller[3]) < 1000):
                        motor.run_speed(1, -1*duty_cycle)
                        motor.run_speed(2, 0*duty_cycle)
                        motor.run_speed(3, 0*duty_cycle)
                        motor.run_speed(4, 1*duty_cycle)
                    else:
                        print("BACKWARRD")
                        motor.run_speed(1, -1*duty_cycle)
                        motor.run_speed(2, 1*duty_cycle)
                        motor.run_speed(3, -1*duty_cycle)
                        motor.run_speed(4, 1*duty_cycle)
                elif (int(controller[3]) > 1004):  # Right
                    duty_cycle2= map_range(
                        int(controller[3]), 1004, 1722, 0, 500)
                    duty_cycle = map_range(
                        int(controller[2]), 1000, 282, 0, 1000)
                    if (int(controller[2]) < 1000):
                        motor.run_speed(1, -1*duty_cycle)
                        motor.run_speed(2, 1*duty_cycle)
                        motor.run_speed(3, 1*duty_cycle)
                        motor.run_speed(4, -1*duty_cycle)
                    elif (int(controller[2]) > 1004):
                        motor.run_speed(1, 1*duty_cycle)
                        motor.run_speed(2, -1*duty_cycle)
                        motor.run_speed(3, -1*duty_cycle)
                        motor.run_speed(4, 1*duty_cycle)
                    else:
                        motor.run_speed(1, 1*duty_cycle2)
                        motor.run_speed(2, 1*duty_cycle2)
                        motor.run_speed(3, -1*duty_cycle2)
                        motor.run_speed(4, -1*duty_cycle2)
                elif (int(controller[3]) < 1000):  # Left
                    duty_cycle2 = map_range(
                        int(controller[3]), 1000, 282, 0, 500)
                    duty_cycle = map_range(
                        int(controller[2]), 1004, 1722, 0, 500)
                    if (int(controller[2]) > 1004):
                        motor.run_speed(1, -1*duty_cycle)

                        motor.run_speed(2, 1*duty_cycle)
                        motor.run_speed(3, 1*duty_cycle)
                        motor.run_speed(4, -1*duty_cycle)
                    elif (int(controller[2]) > 1004):
                        motor.run_speed(1, -1*duty_cycle)
                        motor.run_speed(2, 1*duty_cycle)
                        motor.run_speed(3, -1*duty_cycle)
                        motor.run_speed(4, 1*duty_cycle)
                    else:
                        motor.run_speed(3, 1*duty_cycle2)
                        motor.run_speed(4, 1*duty_cycle2)
                        motor.run_speed(1, -1*duty_cycle2)
                        motor.run_speed(2, -1*duty_cycle2)
                elif (int(controller[4]) == 282):
                    duty_cycle = map_range(
                        int(controller[3]), 1004, 1722, 0, 300)
                    motor.run_speed(1, 1*100)
                    motor.run_speed(2, 1*100)
                    motor.run_speed(3, 1*100)
                    motor.run_speed(4, 1*100)
                elif (int(controller[4]) == 1722):
                    duty_cycle = map_range(
                        int(controller[3]), 1000, 282, 0, 300)
                    motor.run_speed(1, -1*100)
                    motor.run_speed(2, -1*100)
                    motor.run_speed(3, -1*100)
                    motor.run_speed(4, -1*100)
                # elif(int(controller[6])==1722) : #backward_pickup
                #     if(reload == 1):
                #         motor.runInc_speed(1,-360 ,1) #4225  4225
                #         motor.runInc_speed(2,360 ,1)
                #         motor.runInc_speed(3,-360 ,1)
                #         motor.runInc_speed(4,360 ,1)
                #         com.ser.write("Pickup".encode())
                #         # time.sleep(5)
                #         reload = 0
                #     else:
                #         reload = 1
                else:
                    motor.run_speed(1, 0)
                    motor.run_speed(2, 0)
                    motor.run_speed(3, 0)
                    motor.run_speed(4, 0)
                # else:
                #     motor.run_speed(1, 0)
                #     motor.run_speed(2, 0)
                #     motor.run_speed(3, 0)
                #     motor.run_speed(4, 0)
            else:
                motor.run_speed(1, 0)
                motor.run_speed(2, 0)
                motor.run_speed(3, 0)
                motor.run_speed(4, 0)
                
# global reload

def testing():
    
        motor.runInc_speed(1,1 ,4225) #10
        motor.runInc_speed(2,1 ,-4225)
        motor.runInc_speed(3,1 ,4225)
        motor.runInc_speed(4,1 ,-4225)


if __name__ == '__main__':

    thread1 = threading.Thread(target=com.read_from_port, args=(com.ser,))
    thread1.start()

    thread2 = threading.Thread(target=can.read_from_port, args=(can.ser,))
    thread2.start()
    
    thread3 = threading.Thread(target=mainprog) 
    thread3.start()

    # thread4 = threading.Thread(target=testing) 
    # thread4.start()



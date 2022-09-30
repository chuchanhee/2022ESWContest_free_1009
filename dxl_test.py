from dxl_control2.Ax12 import Ax12
from dxl_control2 import teaching_value as tvalue
from threading import Thread
from multiprocessing import Process
import time

# 모터 이름 생성
my_dxl11 = Ax12(11)
my_dxl12 = Ax12(12)
my_dxl13 = Ax12(13)
my_dxl14 = Ax12(14)
my_dxl15 = Ax12(15)

# connecting
Ax12.open_port()
Ax12.set_baudrate()
# motor_object.get_position()

a = 0
b = 0
# 자료 불러오기



Data_Ax12_11 = Ax12(11)
Data_Ax12_12 = Ax12(12)
Data_Ax12_13 = Ax12(13)
Data_Ax12_14 = Ax12(14)
Data_Ax12_15 = Ax12(15)


# 모터 초기세팅 [ 속도 및 각도 한계 제한]

def initial_setting11(my_dxl11):
    my_dxl11.set_ccw_angle_limit(1000)
    my_dxl11.set_cw_angle_limit(150)
    my_dxl11.set_moving_speed(100)
def initial_setting12(my_dxl12):
    my_dxl12.set_ccw_angle_limit(800)
    my_dxl12.set_cw_angle_limit(170)
    my_dxl12.set_moving_speed(50)
def initial_setting13(my_dxl13):
    my_dxl13.set_ccw_angle_limit(800)
    my_dxl13.set_cw_angle_limit(170)
    my_dxl13.set_moving_speed(60)
def initial_setting14(my_dxl14):
    my_dxl14.set_ccw_angle_limit(870)
    my_dxl14.set_cw_angle_limit(188)
    my_dxl14.set_moving_speed(50)
def initial_setting15(my_dxl15):
    my_dxl15.set_ccw_angle_limit(600)
    my_dxl15.set_cw_angle_limit(110)
    my_dxl15.set_moving_speed(50)


initial_setting11(my_dxl11)
initial_setting12(my_dxl12)
initial_setting13(my_dxl13)
initial_setting14(my_dxl14)
initial_setting15(my_dxl15)
def Motor_Complite_check_3():
    while (True):
        returnRun_11 = Data_Ax12_11.is_moving()
        returnRun_12 = Data_Ax12_12.is_moving()
        returnRun_13 = Data_Ax12_13.is_moving()
        returnRun_14 = Data_Ax12_14.is_moving()
        returnRun_15 = Data_Ax12_15.is_moving()

        if returnRun_11 == 0 and returnRun_12 == 0 and returnRun_13 == 0 and returnRun_14 == 0 and returnRun_15 == 0:
            break


def Home_pos(motor_object,servo11_Home1, motion_no):
    motor_object.set_position(servo11_Home1[motion_no])
    my_dxl12.set_position(tvalue.servo12_Home1[motion_no])
    my_dxl13.set_position(tvalue.servo13_Home1[motion_no])
    my_dxl14.set_position(tvalue.servo14_Home1[motion_no])
    my_dxl15.set_position(tvalue.servo15_Home1[motion_no])
def THREE_First_Pos(motor_object,servo11_Pos1, motion_no):
    motor_object.set_position(servo11_Pos1[motion_no])
    my_dxl12.set_position(tvalue.servo12_Pos1[motion_no])
    my_dxl13.set_position(tvalue.servo13_Pos1[motion_no])
    my_dxl14.set_position(tvalue.servo14_Pos1[motion_no])
    my_dxl15.set_position(tvalue.servo15_Pos1[motion_no])





#Home_pos(my_dxl1,tvalue.servo1_Home1,1)


def RB3_POS1():
    step3 = 0
    if step3 ==0:
        for step in range(0,6):
            Motor_Complite_check_3()
            THREE_First_Pos(my_dxl11,tvalue.servo11_Pos1,step3)
            step3 += 1
            if step3 == 6:
                Motor_Complite_check_3()
                THREE_First_Pos(my_dxl11,tvalue.servo11_Pos1,0)
                break

THREE_First_Pos(my_dxl11,tvalue.servo12_Pos1,0)

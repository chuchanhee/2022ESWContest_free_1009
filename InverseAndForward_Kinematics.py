import numpy as np
import math
import matplotlib.pyplot as plt

# Link Parameters
l1 = 0.3; l2 = 1.3; l3 = 2.2
from TCP_PLC.main_detect import Center_Value_list
global th1
th1 =(math.radians(-86))

def invers_Value(Center_Value):
    Center_Value_list[0] = Center_Value[0]
    test = Center_Value_list[0]
    global th1
    if test > 0:
        if 360 < test < 370:
            th1 = (math.radians(-85.6))
        if 350 < test < 360:
            th1 = (math.radians(-85.7))
        if 340 < test < 350:
            th1 = (math.radians(-85.8))
        if 330 < test < 340:
            th1 = (math.radians(-85.9))
        if 320 < test < 330:
            th1 = (math.radians(-86.0))
        if 310 < test < 320:
            th1 = (math.radians(-86.1))
        if 300 < test < 310:
            th1 = (math.radians(-86.2))

    else:
        pass

    # print(th1)
    # print(test)

    th2 = (math.radians(20))
    th3 = (math.radians(-30))


    # Forward Kinematics
    x = np.cos(th1) * (l2 * np.cos(th2) + l3 * (np.cos(th2 + th3)))
    y = np.sin(th1) * (l2 * np.cos(th2) + l3 * (np.cos(th2 + th3)))
    z = l1 + l2 * np.sin(th2) + l3 * (np.sin(th2 + th3))
    #print("Forward Kinematics :", x, y, z)

    #print("Z value : ",z)
    x0 = x
    y0 = y
    xd = x0
    yd = y0
    zd = z

    # Inverse Kinematics
    d = np.sqrt(xd**2 + yd**2 + (zd-l1)**2)
    a = (d**2 - l2**2 -l3**2)/(2*l2*l3)
    theta3 = math.atan2(-np.sqrt(1-a**2), a)
    alpha = math.atan2(zd-l1, np.sqrt(xd**2 + yd**2))
    E = (l2**2 + d**2 -l3**2)/(2*l2*d)
    beta = math.atan2(np.sqrt(1-E**2), E)
    theta2 = alpha + beta
    theta1 = math.atan2(yd, xd)
    #print("Inverse Kinematics :", math.degrees(theta1), math.degrees(theta2), math.degrees(theta3))



#22.05.30
#theta = -86.13, Angle1 = 215



    Angle1 = int(round((math.degrees(theta1)/0.29) + 512,0))

    Angle2 = int(round(512-(math.degrees(theta2)/0.29),0))
    Angle3 = int(round((math.degrees(theta3)/0.29) + 512,0))

    # print(Angle1)
    return Angle1




#####################################################################################
import serial

import dxl_control.dxl_test
from absl import app, flags, logging
from absl.flags import FLAGS
import sys
sys.path.append('/C:/Users/Yun/Desktop/cont_v2/rolypoly2/TCP_PLC/core/utils.py')

from PIL import Image
import cv2
import numpy as np
from multiprocessing import queues
#####################################################################################
import sys, cv2
import time


from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, \
    QPushButton, QApplication, QFrame, QDialog, QLabel
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot, QSize
from PyQt5.QtGui import QImage, QPixmap
from threading import Thread as TH
from multiprocessing import Queue
import TCP_PLC.TCP
from TCP_PLC.TCP import drying_socket
from absl import app as app_2
from TCP_PLC import InverseAndForward_Kinematics as Invk

class Thread2(QThread):
   changePixmap1 = pyqtSignal(QImage)

   def __init__(self, parent=None):
       super().__init__()
       self.n = 0
       self.main = parent
       self.isRun = False
       self.Symbol_1 = False
       self.Symbol_2 = False
       self.Symbol_3 = False

       self.input_size = 416

   def run(self):
       cap1 = self.VideoCapture('http://192.168.0.7:81/stream')
       # cap1 = self.VideoCapture(0)

       while self.isRun:
           ret2, frame2 = cap1.read()

           if ret2:
               frame3 = cv2.resize(frame2, (640,480), interpolation=cv2.INTER_LINEAR)
               frame3 = cv2.flip(frame3,0)
               frame3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2RGB)
               convertToQtFormat2 = QImage(frame3.data, frame3.shape[1], frame3.shape[0], frame3.strides[0], QImage.Format_RGB888)
               q = convertToQtFormat2.scaled(640, 480, Qt.KeepAspectRatio)
               self.changePixmap1.emit(q)

   def VideoCapture(self, port2):
       port2 = 'http://192.168.0.7:81/stream'
       # port2 = 0
       cap1 = cv2.VideoCapture(port2)

       return cap1

################################################################################################################################################
# class bluetooth():
#     receive_data = Queue()
#
#     def __init__(self):
#         self.ser = serial.Serial(port="COM17", baudrate=9600, timeout=1)
#
#     def send_data(self):
#         while True:
#             recdata = self.receive_data.get()
#             recdata1 = str(recdata)
#             print(recdata1)
#             op = recdata1.encode('utf-8')
#             self.ser.write(op)
#             print(op)
#####################################################################################################################################################


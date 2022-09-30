#####################################################################################
import tensorflow as tf
import dxl_control.dxl_test

physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
from absl import app, flags, logging
from absl.flags import FLAGS
import sys
sys.path.append('/C:/Users/Yun/Desktop/cont_v2/rolypoly2/TCP_PLC/core/utils.py')
import core.utils as utils
from core.yolov4 import filter_boxes
from tensorflow.python.saved_model import tag_constants
from PIL import Image
import cv2
import numpy as np
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
import mobility_robot
#####################################################################################
import sys, cv2
import time

import smtplib
from email.mime.text import MIMEText

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

prev_time = 0



framework = 'tf' #'tflite' # tf, tflite, trt
weights = './checkpoints/yolov4-416' #'./checkpoints/yolov4-416.tflite'
size = 416 # resize images to
tiny = False  # 'yolo or yolo-tiny'
model = 'yolov4' # yolov3 or yolov4
iou = 0.30 # iou threshold
score = 0.75 # score threshold
global Center_Value_list
Center_Value_list =[0,0]

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    def __init__(self, parent=None):
        super().__init__()
        self.n = 0
        self.main = parent
        self.isRun = False
        self.Symbol_1 = False
        self.Symbol_2 = False
        self.Symbol_3 = False
#        config = ConfigProto()
#        config.gpu_options.allow_growth = True
#        session = InteractiveSession(config=config)
#        STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config(FLAGS)
#        self.input_size = FLAGS.size
#        video_path = FLAGS.video

        self.input_size = 416


    def run(self):
        cap = self.VideoCapture(0)
        #autofocus 기능 설치 금지

        ################################################################
        ## Yolo Algo Run
        if framework == 'tflite':
            interpreter = tf.lite.Interpreter(model_path=FLAGS.weights)
            interpreter.allocate_tensors()
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            print(input_details)
            print(output_details)
        else:
            saved_model_loaded = tf.saved_model.load(weights, tags=[tag_constants.SERVING])
            infer = saved_model_loaded.signatures['serving_default']

        """(after)
        if FLAGS.output:
            # by default VideoCapture returns float instead of int
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            codec = cv2.VideoWriter_fourcc(*FLAGS.output_format)
            out = cv2.VideoWriter(FLAGS.output, codec, fps, (width, height))
        """
        ########################################################################################


        while self.isRun:
            ret, frame = cap.read()


            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)

                image_data = cv2.resize(frame, (self.input_size, self.input_size))
                image_data = image_data / 255.
                image_data = image_data[np.newaxis, ...].astype(np.float32)
                prev_time = time.time()

                if framework == 'tflite':
                    interpreter.set_tensor(input_details[0]['index'], image_data)
                    interpreter.invoke()
                    pred = [interpreter.get_tensor(output_details[i]['index']) for i in range(len(output_details))]
                    if model == 'yolov3' and tiny == True:
                        boxes, pred_conf = filter_boxes(pred[1], pred[0], score_threshold=0.25,
                                                        input_shape=tf.constant([self.input_size, self.input_size]))
                    else:
                        boxes, pred_conf = filter_boxes(pred[0], pred[1], score_threshold=0.25,
                                                        input_shape=tf.constant([self.input_size, self.input_size]))
                else:
                    batch_data = tf.constant(image_data)
                    pred_bbox = infer(batch_data)
                    for key, value in pred_bbox.items():
                        boxes = value[:, :, 0:4]
                        pred_conf = value[:, :, 4:]
                boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
                    boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
                    scores=tf.reshape(
                        pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
                    max_output_size_per_class=50,
                    max_total_size=50,
                    iou_threshold=iou,
                    score_threshold=score
                )

                PLC_DATA = TCP_PLC.TCP.drying_socket.que
                if PLC_DATA == hex(0x2): # ROBOT 1 REQ 신호
                    if (int(classes[0][0])) ==0 or (int(classes[0][0])) ==2 or (int(classes[0][0])) ==4:
                        time.sleep(1)
                        print("TRUE POSITION MOVE")
                        drying_socket.write_contact.put(0x4)
                    if (int(classes[0][0])) ==1 or (int(classes[0][0])) ==3 or (int(classes[0][0])) ==5:
                        time.sleep(1)
                        print("FALSE POSITION MOVE")
                        drying_socket.write_contact.put(0x5)


                pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]
                image,Center_Value = utils.draw_bbox(frame, pred_bbox)

                global Center_Value_list
                Center_Value_list.insert(0,Center_Value)

                Angle1 = Invk.invers_Value(Center_Value_list)
                dxl_control.dxl_test.return_angle(Angle1)


                del Center_Value_list[1:]
                curr_time = time.time()
                exec_time = curr_time - prev_time

                #result_Video = np.asarray(image)
                info = "time: %.2f ms" % (1000 * exec_time)
                #print(info)

                ###################################################################################
                #rgbImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                rgbImage = image
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                ###################################################################################

    def VideoCapture(self, port):
        port = 0
        cap = cv2.VideoCapture(port)
        return cap
#########################################################################################################
#22.07.05


class MyApp(QMainWindow):


    def setImage(self, image):
        self.vidio_camera.setPixmap(QPixmap.fromImage(image))

    def setImage2(self, image2):
        self.vidio_camera2.setPixmap(QPixmap.fromImage(image2))

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Video'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 600
        self.initUI()
################################################################################
        self.smtpName = "smtp.naver.com"
        self.smtPort = 587

        self.sendEmail = "nill1406@naver.com"
        self.password = "nill1409"
        self.receveEmail = "nill1409@daum.net"

        self.title = "위급 사항"
        self.content = "공정에 문제가 생겼으므로 신속히 복귀하시기 바랍니다."
############################################################################


    def initUI(self) -> object:
        font = QFont('Black')
        font.setPointSize(32)

        font2 = QFont('White')
        font2.setPointSize(30)
#####################################################




        ## QThread
        th = Thread(self)
        th.isRun = True

        th.changePixmap.connect(self.setImage)
        th.start()


        th2 = mobility_robot.Thread2(self)
        th2.isRun = True
        th2.changePixmap1.connect(self.setImage2)
        th2.start()
        ######################################
        #22.05.12__ GUI CAMERA+ CAMERA 표시+ WINDOW 창+ 제목 창

        # camera동영상
        self.vidio_camera= QLabel(self) #label to show face with ROIs
        self.vidio_camera.setGeometry(180,200,640, 480)
        self.vidio_camera.setStyleSheet("background-color: #000000")


        # Camera 표시
        self.Camera1 = QLabel(self)  # label to show stable HR
        self.Camera1.setGeometry(345, 130, 700, 50)
        self.Camera1.setFont(font)
        self.Camera1.setText("<Smart Factory>")
        self.Camera1.setStyleSheet("Color : black")  # 글자색 변환

        self.w_title = QLabel(self)  # label to show stable HR
        self.w_title.setGeometry(720, 12, 580, 80)
        self.w_title.setFont(font)
        self.w_title.setText("   Smart Industrial System")
        self.w_title.setStyleSheet("Color : green;"
                                   "border-style: solid;" "border-width: 3px;"
                                   "border-color: green;" "border-radius: 3px")  # 글자색 변환
        ##############################################################
        # camera동영상
        self.vidio_camera2= QLabel(self) #label to show face with ROIs
        self.vidio_camera2.setGeometry(1140,200,640, 480)
        self.vidio_camera2.setStyleSheet("background-color: #000000")


        # Camera 표시
        self.Camera2 = QLabel(self)  # label to show stable HR
        self.Camera2.setGeometry(1280, 130, 700, 50)
        self.Camera2.setFont(font)
        self.Camera2.setText("<Mobility System>")
        self.Camera2.setStyleSheet("Color : black")  # 글자색 변환



        # 윈도우 설정
        self.setGeometry(0, 0, 1000, 1000)  # x, y, w, h
        self.setWindowTitle('QFrame Window')
        self.setStyleSheet('background:white;')
        self.setFixedSize(1920, 1000)



        ###########################################################

        # QDialog 설정
        self.dialog = QDialog()

        # 스마트팩토리 초기화면 윈도우 설정
        self.setGeometry(300, 300, 500, 300)  # x, y, w, h
        self.setWindowTitle('SMART FACTORY')

        # 초기화면 이벤트 발생 버튼(클릭 하는 순간 이벤트 발생)
        self.pb_pressed0 = QPushButton('생산 시작 ', self)
        self.pb_pressed0.setGeometry(120, 700, 330, 80)
        self.pb_pressed0.setFont(font)
        self.pb_pressed0.pressed.connect(self.button_pressed)
        self.pb_pressed0.setStyleSheet("Color : blue;" "border-color: blue;" 
                                       "border-radius: 3px;" "border-style: solid;" "border-width: 3px;")

        self.pb_pressed1 = QPushButton('창고 취출실린더 ', self)
        self.pb_pressed1.setGeometry(120, 800, 330, 80)
        self.pb_pressed1.setFont(font)
        self.pb_pressed1.pressed.connect(self.button_pressed_1)
        self.pb_pressed1.setStyleSheet("border-color: black;" "border-radius: 3px;" "border-style: solid;" "border-width: 3px;")


        self.pb_pressed2 = QPushButton('메거진 실린더 ', self)
        self.pb_pressed2.setGeometry(120, 900, 330, 80)
        self.pb_pressed2.setFont(font)
        self.pb_pressed2.pressed.connect(self.button_pressed_2)
        self.pb_pressed2.setStyleSheet("border-color: black;" "border-radius: 3px;" "border-style: solid;" "border-width: 3px;")

        self.pb_pressed3 = QPushButton('CV1 기동 ', self)
        self.pb_pressed3.setGeometry(550, 700, 330, 80)
        self.pb_pressed3.setFont(font)
        self.pb_pressed3.pressed.connect(self.button_pressed_3)
        self.pb_pressed3.setStyleSheet("border-color: black;" "border-radius: 3px;" "border-style: solid;" "border-width: 3px;")

        self.pb_pressed4 = QPushButton('CV2 기동 ', self)
        self.pb_pressed4.setGeometry(550, 800, 330, 80)
        self.pb_pressed4.setFont(font)
        self.pb_pressed4.pressed.connect(self.button_pressed_4)
        self.pb_pressed4.setStyleSheet("border-color: black;" "border-radius: 3px;" "border-style: solid;" "border-width: 3px;")

        self.pb_pressed5 = QPushButton('CV3 기동 ', self)
        self.pb_pressed5.setGeometry(550, 900, 330, 80)
        self.pb_pressed5.setFont(font)
        self.pb_pressed5.pressed.connect(self.button_pressed_5)
        self.pb_pressed5.setStyleSheet("border-color: black;" "border-radius: 3px;" "border-style: solid;" "border-width: 3px;")
#22.07.05
        ##################################################
        self.pb_pressed6 = QPushButton('긴급사항 전달',self)
        self.pb_pressed6.setGeometry(1090, 780, 320, 70)
        self.pb_pressed6.setFont(font)
        self.pb_pressed6.pressed.connect(self.button_pressed_6)
        self.pb_pressed6.setStyleSheet("Color : Red;" "border-color: Red;" "border-style: outset;" "border-width: 4px;")

        self.pb_pressed7 = QPushButton('긴급상황 발생 ', self)
        self.pb_pressed7.setGeometry(1090, 700, 320, 70)
        self.pb_pressed7.setFont(font)
        self.pb_pressed7.pressed.connect(self.button_pressed_7)
        self.pb_pressed7.setStyleSheet("Color : Red;" "border-color: Red;" "border-style: outset;" "border-width: 4px;")

        self.pb_pressed8 = QPushButton('수동 ', self)
        self.pb_pressed8.setGeometry(1090, 860, 320, 65)
        self.pb_pressed8.setFont(font2)
        self.pb_pressed8.pressed.connect(self.button_pressed_8)
        self.pb_pressed8.setStyleSheet("Color : White;"
                                   "background-color: Blue;")

        self.pb_pressed9 = QPushButton('자동 ', self)
        self.pb_pressed9.setGeometry(1090, 930, 320, 65)
        self.pb_pressed9.setFont(font2)
        self.pb_pressed9.pressed.connect(self.button_pressed_9)
        self.pb_pressed9.setStyleSheet("Color : White;"
                                   "background-color: Green;")

        self.pb_pressed10 = QPushButton(self)
        self.pb_pressed10.setGeometry(1570, 690, 100, 100)
        self.pb_pressed10.setIcon(QIcon('./images/up_arrow.jpg'))
        self.pb_pressed10.setIconSize(QSize(90,100))
        self.pb_pressed10.pressed.connect(self.button_pressed_10)
        self.pb_pressed10.setStyleSheet("border-color: Black;" "border-style: outset;" "border-width: 4px;")

        self.pb_pressed11 = QPushButton(self)
        self.pb_pressed11.setGeometry(1570, 890, 100, 100)
        self.pb_pressed11.setIcon(QIcon('./images/down_arrow.jpg'))
        self.pb_pressed11.setIconSize(QSize(90,100))
        self.pb_pressed11.pressed.connect(self.button_pressed_11)
        self.pb_pressed11.setStyleSheet("border-color: Black;" "border-style: outset;" "border-width: 4px;")

        self.pb_pressed12 = QPushButton(self)
        self.pb_pressed12.setGeometry(1470, 790, 100, 100)
        self.pb_pressed12.setIcon(QIcon('./images/left_arrow.jpg'))
        self.pb_pressed12.setIconSize(QSize(90,100))
        self.pb_pressed12.pressed.connect(self.button_pressed_12)
        self.pb_pressed12.setStyleSheet("border-color: Black;" "border-style: outset;" "border-width: 4px;")

        self.pb_pressed13 = QPushButton(self)
        self.pb_pressed13.setGeometry(1670, 790, 100, 100)
        self.pb_pressed13.setIcon(QIcon('./images/right_arrow.jpg'))
        self.pb_pressed13.setIconSize(QSize(90,100))
        self.pb_pressed13.pressed.connect(self.button_pressed_13)
        self.pb_pressed13.setStyleSheet("border-color: Black;" "border-style: outset;" "border-width: 4px;")
########################################################################################################################
        # self.pb_pressed14 = QPushButton(self)
        # self.pb_pressed14.setGeometry(1620, 790, 50, 100)
        # self.pb_pressed14.setIcon(QIcon('./images/r_cir.png'))
        # self.pb_pressed14.setIconSize(QSize(40,100))
        # self.pb_pressed14.pressed.connect(self.button_pressed_14)
        # self.pb_pressed14.setStyleSheet("border-color: Black;" "border-style: outset;" "border-width: 4px;")
        #
        # self.pb_pressed15 = QPushButton(self)
        # self.pb_pressed15.setGeometry(1570, 790, 50, 100)
        # self.pb_pressed15.setIcon(QIcon('./images/l_cir.png'))
        # self.pb_pressed15.setIconSize(QSize(40,100))
        # self.pb_pressed15.pressed.connect(self.button_pressed_15)
        # self.pb_pressed15.setStyleSheet("border-color: Black;" "border-style: outset;" "border-width: 4px;")
########################################################################################################################
        self.pb_pressed16 = QPushButton(self)
        self.pb_pressed16.setGeometry(1570, 790, 100, 100)
        # self.pb_pressed16.setIcon(QIcon('./images/cir.PNG'))
        # self.pb_pressed16.setIconSize(QSize(90,100))
        self.pb_pressed16.pressed.connect(self.button_pressed_16)
        self.pb_pressed16.setStyleSheet("border-color: Black;" "border-style: outset;" "border-width: 4px;")

        # 초기화면 이벤트 발생 버튼(눌렀다가 떼는 순간 이벤트 발생)
        """
        self.pb_released = QPushButton('정지 버튼', self)
        self.pb_released.setGeometry(805, 190, 150, 30)
        self.pb_released.released.connect(self.button_released)
        """

        # 전체화면
        screen = QtWidgets.QDesktopWidget().screenGeometry()

        self.setWindowTitle('스마트팩토리')
        self.setGeometry(0, 0, screen.width(), screen.height())
        self.show()



    def nedialog_open(self):
        # 새창 버튼 실행
        btnDialog = QPushButton("확인", self.dialog)
        btnDialog.move(100, 100)
        btnDialog.clicked.conct(self.dialog_close)

        # 새창 세팅

        self.dialog.setWindowTitle('새창')
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(300, 200)
        self.dialog.show()

    @pyqtSlot()
    def radio_select(self):
        # QRadioButton1 클릭 여부 표시
        if self.radio1.isChecked():
            self.label.setText('이송공정 완료')
        elif self.radio2.isChecked():
            self.label.setText('전체공정 완료')



    def button_pressed(self):
        drying_socket.write_contact.put(0x1c)
    def button_pressed_1(self):
        drying_socket.write_contact.put(0x1a)
    def button_pressed_2(self):
        drying_socket.write_contact.put(0x1b)
    def button_pressed_3(self):
        drying_socket.write_contact.put(0x1d)
    def button_pressed_4(self):
        drying_socket.write_contact.put(0x1e)
    def button_pressed_5(self):
        drying_socket.write_contact.put(0x1f)


################################################
    def button_pressed_6(self):
        print("email_pressed")
        msg = MIMEText(self.content)
        msg['From'] = self.sendEmail
        msg['To'] = self.receveEmail
        msg['Subject'] = self.title

        s = smtplib.SMTP(self.smtpName, self.smtPort)
        s.starttls()
        s.login(self.sendEmail, self.password)
        s.sendmail(self.sendEmail, self.receveEmail, msg.as_string())
        s.close()

    def button_pressed_7(self):
        print("긴급상황 발생")
        # mobility_robot.bluetooth.receive_data.put('e')
        drying_socket.write_contact.put(0x20)

    def button_pressed_8(self):
        print("Manual pressed")
        # mobility_robot.bluetooth.receive_data.put('y')

    def button_pressed_9(self):
        print("Auto pressed")
        # mobility_robot.bluetooth.receive_data.put('n')

    def button_pressed_10(self):
        print("up_button pressed")
        # mobility_robot.bluetooth.receive_data.put('w')

    def button_pressed_11(self):
        print("down_button pressed")
        # mobility_robot.bluetooth.receive_data.put('s')

    def button_pressed_12(self):
        print("left_button pressed")
        # mobility_robot.bluetooth.receive_data.put('d')

    def button_pressed_13(self):
        print("right_button pressed")
        # mobility_robot.bluetooth.receive_data.put('a')

    # def button_pressed_14(self):
    #     print("r_cir pressed")
    #     # mobility_robot.bluetooth.receive_data.put('a')
    #
    # def button_pressed_15(self):
    #     print("l_cir pressed")
    #     # mobility_robot.bluetooth.receive_data.put('d')

    def button_pressed_16(self):
        print("rotated pressed")
        # mobility_robot.bluetooth.receive_data.put('u')

    def button_released(self):
        print('정지되었습니다')
        dxl_control.dxl_test.TSET()
    # Dialog 닫기 이벤트
    def dialog_close(self):
        self.dialog.close()



if __name__ == '__main__':
    q = Queue()
    a = TCP_PLC.TCP.drying_socket.mobile_socket()

    Process1= TH(target=a.mobile_bind,args=())
    Process1.start()

    d = drying_socket.PLC_Network()
    print('성공')
    Process2 = TH(target=d.PLC_Connect,args=())
    Process2.start()

    # e = mobility_robot.Thread2()
    # process3 = TH(target=e.run(),args=())
    # process3.start()

    # f = mobility_robot.bluetooth()
    # process3 = TH(target=f.send_data , args=())
    # process3.start()

    app = QApplication(sys.argv)
    ex = MyApp()

    ex.show()
    sys.exit(app.exec_())

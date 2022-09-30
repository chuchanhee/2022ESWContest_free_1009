"""
#from dxl_control import InverseAndForward_Kinematics as Invki
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtCore
from multiprocessing import Process, freeze_support, Queue
from TCP_PLC.TCP import client
from socket import *
import sys, threading, cv2, dlib
import os, glob, numpy as np
from keras.models import load_model
'''
IP1 = '192.168.10.20'
PORT1 = 502
'''
class Course_main(QDialog):
    def __init__(self):
        super().__init__()
        self.Course_window()
    def Course_window(self):
        self.setWindowTitle('코스 선택 화면')
        self.setFixedSize(1920, 1300)

        btn_course_1 = QPushButton('', self)  # Drying 시작 -> 다음 화면으로 넘어감 ->코스 1버튼 250, 125
        btn_course_1.setIcon(QtGui.QIcon("img/course_1.png"))
        btn_course_1.setIconSize(QtCore.QSize(180, 180))
        btn_course_1.setStyleSheet('border:0px;')
        btn_course_1.move(600, 420)
        btn_course_1.clicked.connect(self.course_1_btn)

        btn_course_2 = QPushButton('', self)  # Drying 시작 -> 다음 화면으로 넘어감 ->코스 2버튼
        btn_course_2.setIcon(QtGui.QIcon("img/course_2.png"))
        btn_course_2.setIconSize(QtCore.QSize(180, 180))
        btn_course_2.setStyleSheet('border:0px;')
        btn_course_2.move(850, 420)
        btn_course_2.clicked.connect(self.course_2_btn)

        btn_course_3 = QPushButton('', self)  # Drying 시작 -> 다음 화면으로 넘어감 ->코스 3버튼
        btn_course_3.setIcon(QtGui.QIcon("img/course_3.png"))
        btn_course_3.setIconSize(QtCore.QSize(180, 180))
        btn_course_3.setStyleSheet('border:0px;')
        btn_course_3.move(1100, 420)
        btn_course_3.clicked.connect(self.course_3_btn)

        btn_open_door = QPushButton('', self)  # Drying 시작 -> 다음 화면으로 넘어감 ->문 열기
        btn_open_door.setIcon(QtGui.QIcon("img/icons_open_door.png"))
        btn_open_door.setIconSize(QtCore.QSize(130, 130))
        btn_open_door.setStyleSheet('border:0px;')
        btn_open_door.move(1550, 800)
        btn_open_door.clicked.connect(self.open_door_btn)

        btn_undo = QPushButton('', self)  # Drying 시작 -> 다음 화면으로 넘어감 ->이전 화면
        btn_undo.setIcon(QtGui.QIcon("img/icons_undo.png"))
        btn_undo.setIconSize(QtCore.QSize(130, 130))
        btn_undo.setStyleSheet('border:0px;')
        btn_undo.move(1700, 800)
        btn_undo.clicked.connect(self.undo_btn)

    def course_1_btn(self): # 코스 1 버튼
        IP1 = '192.168.10.20'
        PORT1 = 502
        s = socket(AF_INET, SOCK_STREAM)
        try:
            s.connect((IP1,PORT1))
            print("PLC connect success")
        except:
            print("failed")
        p2 = Process(target=client.write_frame, args=(0x55, 1, s))  # args=(memory_number, on&off, soket) p2join set
        p2.start()
        p2.join()
        print("1")

    def course_2_btn(self): # 코스 2 버튼
        IP1 = '192.168.10.20'
        PORT1 = 502
        s = socket(AF_INET, SOCK_STREAM)
        try:
            s.connect((IP1, PORT1))
            print("PLC connect success")
        except:
            print("failed")
        p2 = Process(target=client.write_frame, args=(0x56, 1, s))  # args=(memory_number, on&off, soket) p2join set
        p2.start()
        p2.join()
        print("1")


    def course_3_btn(self): # 코스 3 버튼
        IP1 = '192.168.10.20'
        PORT1 = 502
        s = socket(AF_INET, SOCK_STREAM)
        try:
            s.connect((IP1, PORT1))
            print("PLC connect success")
        except:
            print("failed")
        p2 = Process(target=client.write_frame, args=(0x57, 1, s))  # args=(memory_number, on&off, soket) p2join set
        p2.start()
        p2.join()
        print("1")


    '''
    def course_fast_btn(self): # 코스 급속 버튼
        print("문이 열립니다 ㅋㅋ")
    def course_user1_btn(self): # 사용자 코스1 버튼
        print("문이 열립니다 ㅋㅋ")
    def course_user2_btn(self): # 사용자 코스2 버튼
        print("문이 열립니다 ㅋㅋ")
    '''
    def open_door_btn(self): # 문 열림
        IP1 = '192.168.10.20'
        PORT1 = 502
        s = socket(AF_INET, SOCK_STREAM)
        try:
            s.connect((IP1, PORT1))
            print("PLC connect success")
        except:
            print("failed")
        p2 = Process(target=client.write_frame, args=(0x5a, 1, s))  # args=(memory_number, on&off, soket) p2join set
        p2.start()
        p2.join()
        print("1")
    def undo_btn(self): # 문 열림
        main_return = QMessageBox.question(self, '알림', '이전 화면으로 이동 하시겠습니까?',
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if main_return == QMessageBox.Yes:
            self.close()
            undo = Main_Button_window()
            undo.exec_()
            undo.show()
        else:
            pass

class Add_ons_main(QDialog):  #부가기능 버튼 구성 화면
    def __init__(self):
        super().__init__()
        self.Add_ons_window()

    def Add_ons_window(self): #부가 기능 버튼 -> 메모장, 그림판, 유튜브
        self.setWindowTitle('메모장')
        self.setFixedSize(1920, 1200)

        btn_undo = QPushButton('', self)  # Drying 시작 -> 다음 화면으로 넘어감 ->코스 급속버튼
        btn_undo.setIcon(QtGui.QIcon("img/icons_undo.png"))
        btn_undo.setIconSize(QtCore.QSize(130, 130))
        btn_undo.setStyleSheet('border:0px;')
        btn_undo.clicked.connect(self.undo_btn)

        hbox = QHBoxLayout()
        hbox.addStretch(1)

        hbox.addWidget(btn_undo)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)
    def undo_btn(self): # 이전 화면으로
        main_return = QMessageBox.question(self, '알림', '이전 화면으로 이동 하시겠습니까?',
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if main_return == QMessageBox.Yes:
            self.close()
            undo = Main_Button_window()
            undo.exec_()
            undo.show()
        else:
            pass
class Main_Button_window(QDialog):
    def __init__(self):
        super().__init__()
        self.Good_Drying_Window()
    def Good_Drying_Window(self): #메인화면에 -> (얼굴 인증 화면 부터 먼저) -> Good Drying 버튼을 누르면 나오는 창.
        self.setWindowTitle('Good Drying')
        self.setFixedSize(1920, 1200)

        #상단에 현재 시간 알림

        btn_Drying_start = QPushButton('', self)  #Drying 시작 -> 다음 화면으로 넘어감
        btn_Drying_start.setIcon(QtGui.QIcon("img/icons_shirt.png"))
        btn_Drying_start.setIconSize(QtCore.QSize(180, 180))
        btn_Drying_start.setStyleSheet('border:0px;')
        btn_Drying_start.move(1000, 420)
        btn_Drying_start.clicked.connect(self.Drying_start_btn)

        btn7 = QPushButton('', self) #메인 화면으로 ->초기 화면으로
        btn7.setIcon(QtGui.QIcon("img/icons_home_page.png"))
        btn7.setIconSize(QtCore.QSize(180, 180))
        btn7.setStyleSheet('border:0px;')
        btn7.move(1700, 800)
        btn7.clicked.connect(self.Btn7)

        btn9 = QPushButton('', self) #문 열림 -> 문열림 (닫힘으로 아이콘 바뀔 예정)
        btn9.setIcon(QtGui.QIcon("img/icons_open_door.png"))
        btn9.setIconSize(QtCore.QSize(180, 180))
        btn9.setStyleSheet('border:0px;')
        btn9.move(630, 420)
        btn9.clicked.connect(self.Btn9)

    def Drying_start_btn(self): # Drying 시작 -> 코스 선택화면
        self.close()
        confirm_window = User_conformation_window()
        confirm_window.exec_()
        confirm_window.show()

    def Btn7(self): # 메인 화면 -> 다시 첫 화면
        main_return = QMessageBox.question(self, '알림', '메인 화면으로 이동 하시겠습니까?',
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if main_return == QMessageBox.Yes:
            self.close()
        else:
            pass
    '''
    def add_btn(self): # 부가 기능 -> 메모장, 그림판, 유튜브 선택 창
        self.close()
        Add_ons_window = Add_ons_main()
        Add_ons_window.exec_()
        Add_ons_window.show()
    '''
    def Btn9(self): # 문 열림 ->
        IP1 = '192.168.10.20'
        PORT1 = 502
        s = socket(AF_INET, SOCK_STREAM)
        try:
            s.connect((IP1, PORT1))
            print("PLC connect success")
        except:
            print("failed")
        p2 = Process(target=client.write_frame, args=(0x5a, 1, s))  # args=(memory_number, on&off, soket) p2join set
        p2.start()
        p2.join()
        print("1")


class User_information_window(QDialog): #사용자 정보 창
    global running

    def __init__(self):
        super().__init__()
        self.User_information_UI()
        self.running = False
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    def User_information_UI(self):

        self.setFixedSize(1920, 1200)
        self.setWindowTitle('사용자정보등록')

        self.cpt = cv2.VideoCapture(1)
        self.fps = self.cpt.get(cv2.CAP_PROP_FPS)
        _, self.img_o = self.cpt.read()
        self.img_o = cv2.cvtColor(self.img_o, cv2.COLOR_RGB2GRAY)
        print(self.fps)
        self.cnt = 0
        self.val0 = False
        self.val1 = 0
        self.x = 0
        self.step = 0

        self.mnt = QLabel(self)
        self.mnt.resize(1640, 1000)
        self.mnt.setStyleSheet('border:0px;')
        self.mnt.setScaledContents(True)
        self.mnt.move(1, 1)

        btn_ca = QPushButton('', self)  # Drying 시작 -> 다음 화면으로 넘어감 ->이전 화면
        btn_ca.setIcon(QtGui.QIcon("img/icons_camera_on.png"))
        btn_ca.setIconSize(QtCore.QSize(130, 130))
        btn_ca.setStyleSheet('border:0px;')
        btn_ca.move(1700, 50)
        btn_ca.clicked.connect(self.start)

        btn_caoff = QPushButton('', self)  # Drying 시작 -> 다음 화면으로 넘어감 ->이전 화면
        btn_caoff.setIcon(QtGui.QIcon("img/icons_camera_off.png"))
        btn_caoff.setIconSize(QtCore.QSize(130, 130))
        btn_caoff.setStyleSheet('border:0px;')
        btn_caoff.move(1700, 250)
        btn_caoff.clicked.connect(self.stop)

        btn_dnshot = QPushButton('', self)  # Drying 시작 -> 다음 화면으로 넘어감 ->이전 화면
        btn_dnshot.setIcon(QtGui.QIcon("img/icons_camera_capture.png"))
        btn_dnshot.setIconSize(QtCore.QSize(130, 130))
        btn_dnshot.setStyleSheet('border:0px;')
        btn_dnshot.move(1700, 450)
        btn_dnshot.clicked.connect(self.D_snshot)

        self.pbar = QProgressBar(self)
        self.pbar.resize(200, 30)
        self.pbar.move(1700, 650)


        btn_undo = QPushButton('', self)  # Drying 시작 -> 다음 화면으로 넘어감 ->이전 화면
        btn_undo.setIcon(QtGui.QIcon("img/icons_undo.png"))
        btn_undo.setIconSize(QtCore.QSize(130, 130))
        btn_undo.setStyleSheet('border:0px;')
        btn_undo.move(1700, 800)
        btn_undo.clicked.connect(self.undo_btn)



    def nextFrameSlot(self):
        global running, val0

        while self.running:
            _, self.cam = self.cpt.read()
            self.cam = cv2.cvtColor(self.cam, cv2.COLOR_BGR2RGB)
            self.cam = cv2.flip(self.cam, 1)
            self.scam = self.cam.copy()
            img_gray = cv2.cvtColor(self.cam, cv2.COLOR_BGR2GRAY)
            dets = self.detector(img_gray, 1)

            ALL = list(range(0, 68))  # 얼굴전체
            index = ALL
            self.val1 = 0
            for face in dets:  # upsampling 검출된 얼굴 화면 갯수 만큼 반복
                shape = self.predictor(self.cam, face)  # 얼굴에서 68개 점 찾기

                list_points = []  # 검출된 랜드마크 리스트에 저장
                for p in shape.parts():
                    list_points.append([p.x, p.y])

                list_points = np.array(list_points)  # 리스트를 numpy 배열로 변환

                for i, pt in enumerate(list_points[index]):  # 검출된 랜드마크 중 index 변수에 지정된 부위만 이미지에 출력
                    pt_pos = (pt[0], pt[1])
                    cv2.circle(self.cam, pt_pos, 2, (0, 255, 0), -1)

                cv2.rectangle(self.cam, (face.left(), face.top()), (face.right(), face.bottom()),
                              # 검출된 얼굴 영역에 빨간색 사각형 출력
                              (0, 0, 255), 3)

                self.src = self.scam[face.top() - 50: face.bottom() + 50, face.left() - 50:face.right() + 50]
                self.val1 = 1

            self.img_p = cv2.cvtColor(self.cam, cv2.COLOR_RGB2GRAY)
            self.img_o = self.img_p.copy()
            img =QtGui.QImage(self.cam, self.cam.shape[1], self.cam.shape[0], QtGui.QImage.Format_RGB888)
            pix = QtGui.QPixmap.fromImage(img)
            self.mnt.setPixmap(pix)

    #버튼 중 start, stop, snapshot을 클릭시 각 해당 함수 실행

    def start(self):
        global running
        self.running = True
        self.th = threading.Thread(target=self.nextFrameSlot)
        self.th.start()

    def stop(self):
        global running
        self.frame.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage()))
        self.running = False

    def D_snshot(self):
        self.n = 1400
        print(self.n)
        while self.x <= self.n:
            self.cnt += 1
            self.pbar.setValue(self.step)
            if self.cnt % (self.fps * 1000) == 0:
                print(self.val1)
                if self.val1:
                    print(self.cnt)
                    self.src = cv2.cvtColor(self.src, cv2.COLOR_RGB2BGR)
                    cv2.imwrite('./data/dt/ds/jm/' + str(self.x) + '.jpg', self.src)
                    self.x += 1
                    self.step = int(self.x / self.n * 100)

                else:
                    print(self.val1)
                    self.cnt = 0

            if self.x == 1401:
                self.x = 0
                break

    def undo_btn(self):  # 이전 화면으로
        main_return = QMessageBox.question(self, '알림', '이전 화면으로 이동 하시겠습니까?',
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if main_return == QMessageBox.Yes:
            self.close()
            undo = Main_Button_window()
            undo.exec_()
            undo.show()
        else:
            pass

class User_UI_Window(QDialog): # 사용자 추가 등록 & 메인 선택 화면
    def __init__(self):
        super().__init__()
        self.User_Select()

    def User_Select(self):
        self.setWindowTitle('사용자 추가 등록 & 메인 선택 화면')
        self.setFixedSize(600, 400)

        btn_user_plus = QPushButton('',self) ##사용자 추가
        btn_user_plus.setIcon(QtGui.QIcon("img/icons_user+.png"))
        btn_user_plus.setIconSize(QtCore.QSize(180, 180))
        btn_user_plus.setStyleSheet('border:0px;')
        btn_user_plus.clicked.connect(self.user_plus_btn)
        btn_user_plus.resize(60, 90)

        btn_back = QPushButton('',self) ## 메인화면으로 돌아가기
        btn_back.setIcon(QtGui.QIcon("img/icons_home_page.png"))
        btn_back.setIconSize(QtCore.QSize(180, 180))
        btn_back.setStyleSheet('border:0px;')
        btn_back.clicked.connect(self.back_btn)
        btn_back.resize(60, 90)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn_user_plus)
        hbox.addWidget(btn_back)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)

    def user_plus_btn(self):  #사용자 추가 -> 캡쳐 시작
        self.close()
        User_Image_Cap = User_Image_Window()
        User_Image_Cap.exec_()
        User_Image_Cap.show()


    def back_btn(self): #메인 화면으로
        main_return = QMessageBox.question(self, '알림', '메인 화면으로 이동 하시겠습니까?',
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if main_return == QMessageBox.Yes:
            self.close()
        else:
            pass

class Main_Window(QDialog): #메인 메뉴 창
    def __init__(self):
        super().__init__()
        self.initUI()
        self.center()  # 창이 화면 가운데에 위치하게 한다.
    def initUI(self):
        self.setFixedSize(1920, 1200)  # 가로 세로 창 크기 조절
        self.setWindowTitle('Main')  # 타이틀


        btn_main = QPushButton('',self) # 메인 가운데 버튼 . 클릭시 [사용자 확인]으로 간다.
        btn_main.setIcon(QtGui.QIcon("./img/icons_main.png"))
        btn_main.setIconSize(QtCore.QSize(180,180))
        btn_main.clicked.connect(self.main_btn)
        btn_main.setStyleSheet('border:0px;')
        btn_main.resize(230, 230)
        btn_main.move(780, 420)

        btn_add_user = QPushButton('', self) # 사용자 등록 .
        btn_add_user.setIcon(QtGui.QIcon("img/icons_add_user.png"))
        btn_add_user.setIconSize(QtCore.QSize(180, 180))
        btn_add_user.clicked.connect(self.add_user_btn)
        btn_add_user.setStyleSheet('border:0px;')
        btn_add_user.resize(230, 230)
        btn_add_user.move(50, 800)

    def main_btn(self): # good drying 버튼
        MainButton = Main_Button_window()
        MainButton.exec_()
        MainButton.show()
    def add_user_btn(self): #사용자 등록 버튼
        add_user = User_information_window()
        add_user.exec_()

    def center(self): # 윈도우 창 센터로 하는 명령어
        qr = self.frameGeometry() # 창의 위치와 크기 정보를 가져온다.
        cp = QDesktopWidget().availableGeometry().center() #사용하는 모니터 화면의 가운데 위치를 파악한다.
        qr.moveCenter(cp)   #창의 직사각형 위치를 화면의 중심의 위치로 이동한다.
        self.move(qr.topLeft())

class User_conformation_window(QDialog): #사용자 확인 창
    global running

    def __init__(self):
        super().__init__()
        self.User_information_UI()
        self.running = False
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

    def User_information_UI(self):

        self.setFixedSize(1920, 1200)
        self.setWindowTitle('사용자정보등록')

        self.cpt = cv2.VideoCapture(1)
        self.fps = self.cpt.get(cv2.CAP_PROP_FPS)
        _, self.img_o = self.cpt.read()
        self.img_o = cv2.cvtColor(self.img_o, cv2.COLOR_RGB2GRAY)
        print(self.fps)
        self.cnt = 0
        self.val0 = False
        self.val1 = 0
        self.x = 0
        self.step = 0

        self.mnt = QLabel(self)
        self.mnt.resize(1640, 1000)
        self.mnt.setStyleSheet('border:0px;')
        self.mnt.setScaledContents(True)
        self.mnt.move(1, 1)

        btn_ca = QPushButton('', self)  # Drying 시작 -> 다음 화면으로 넘어감 ->이전 화면
        btn_ca.setIcon(QtGui.QIcon("img/icons_camera_on.png"))
        btn_ca.setIconSize(QtCore.QSize(130, 130))
        btn_ca.setStyleSheet('border:0px;')
        btn_ca.move(1700, 50)
        btn_ca.clicked.connect(self.start)

        btn_caoff = QPushButton('', self)  # Drying 시작 -> 다음 화면으로 넘어감 ->이전 화면
        btn_caoff.setIcon(QtGui.QIcon("img/icons_camera_off.png"))
        btn_caoff.setIconSize(QtCore.QSize(130, 130))
        btn_caoff.setStyleSheet('border:0px;')
        btn_caoff.move(1700, 250)
        btn_caoff.clicked.connect(self.stop)

        btn_dnshot = QPushButton('', self)  # Drying 시작 -> 다음 화면으로 넘어감 ->이전 화면
        btn_dnshot.setIcon(QtGui.QIcon("img/icons_camera_capture.png"))
        btn_dnshot.setIconSize(QtCore.QSize(130, 130))
        btn_dnshot.setStyleSheet('border:0px;')
        btn_dnshot.move(1700, 450)
        btn_dnshot.clicked.connect(self.D_snshot)

        self.pbar = QProgressBar(self)
        self.pbar.resize(200, 30)
        self.pbar.move(1700, 650)


        btn_undo = QPushButton('', self)  # Drying 시작 -> 다음 화면으로 넘어감 ->이전 화면
        btn_undo.setIcon(QtGui.QIcon("img/icons_undo.png"))
        btn_undo.setIconSize(QtCore.QSize(130, 130))
        btn_undo.setStyleSheet('border:0px;')
        btn_undo.move(1700, 800)
        btn_undo.clicked.connect(self.undo_btn)



    def nextFrameSlot(self):
        global running, val0

        while self.running:
            _, self.cam = self.cpt.read()
            self.cam = cv2.cvtColor(self.cam, cv2.COLOR_BGR2RGB)
            self.cam = cv2.flip(self.cam, 1)
            self.scam = self.cam.copy()
            img_gray = cv2.cvtColor(self.cam, cv2.COLOR_BGR2GRAY)
            dets = self.detector(img_gray, 1)

            ALL = list(range(0, 68))  # 얼굴전체
            index = ALL
            self.val1 = 0
            for face in dets:  # upsampling 검출된 얼굴 화면 갯수 만큼 반복
                shape = self.predictor(self.cam, face)  # 얼굴에서 68개 점 찾기

                list_points = []  # 검출된 랜드마크 리스트에 저장
                for p in shape.parts():
                    list_points.append([p.x, p.y])

                list_points = np.array(list_points)  # 리스트를 numpy 배열로 변환

                for i, pt in enumerate(list_points[index]):  # 검출된 랜드마크 중 index 변수에 지정된 부위만 이미지에 출력
                    pt_pos = (pt[0], pt[1])
                    cv2.circle(self.cam, pt_pos, 2, (0, 255, 0), -1)

                cv2.rectangle(self.cam, (face.left(), face.top()), (face.right(), face.bottom()),
                              # 검출된 얼굴 영역에 빨간색 사각형 출력
                              (0, 0, 255), 3)

                self.src = self.scam[face.top() - 50: face.bottom() + 50, face.left() - 50:face.right() + 50]
                self.val1 = 1

            self.img_p = cv2.cvtColor(self.cam, cv2.COLOR_RGB2GRAY)
            self.img_o = self.img_p.copy()
            img =QtGui.QImage(self.cam, self.cam.shape[1], self.cam.shape[0], QtGui.QImage.Format_RGB888)
            pix = QtGui.QPixmap.fromImage(img)
            self.mnt.setPixmap(pix)

    #버튼 중 start, stop, snapshot을 클릭시 각 해당 함수 실행

    def start(self):
        global running
        self.running = True
        self.th = threading.Thread(target=self.nextFrameSlot)
        self.th.start()

    def stop(self):
        global running
        self.frame.setPixmap(QtGui.QPixmap.fromImage(QtGui.QImage()))
        self.running = False

    def D_snshot(self):
        self.n = 5
        print(self.n)
        while self.x <= self.n:
            self.cnt += 1
            self.pbar.setValue(self.step)
            if self.cnt % (self.fps * 1000) == 0:
                print(self.val1)
                if self.val1:
                    print(self.cnt)
                    self.src = cv2.cvtColor(self.src, cv2.COLOR_RGB2BGR)
                    cv2.imwrite('./data/dt/ds/jm_c/' + str(self.x) + '.jpg', self.src)
                    self.x += 1
                    self.step = int(self.x / self.n * 100)

                else:
                    print(self.val1)
                    self.cnt = 0

            if self.x == 6:
                self.x = 0
                if self.x == 0:
                    from DT3_GG import WYA
                    WYA()
                    self.close()
                    cm = Course_main()
                    cm.exec_()
                    cm.show()
                    #self.exit()
                break

    def undo_btn(self):  # 이전 화면으로
        main_return = QMessageBox.question(self, '알림', '이전 화면으로 이동 하시겠습니까?',
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if main_return == QMessageBox.Yes:
            self.close()
            undo = Main_Button_window()
            undo.exec_()
            undo.show()
        else:
            pass



if __name__== '__main__':
    '''
    freeze_support()
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((IP1, PORT1))
    print('PLC connect success')
    q = Queue()  # start
    p = Process(target=client.read_frame, args=(s, q))  # 모니터링
    p.start()
    while True:  # 입력값
        print(q.get())
        p2 = Process(target=client.write_frame, args=(2, 0, s))             #args=(memory_number, on&off, soket) p2join set
        p2.start()
        p2.join()
    '''
    app = QApplication(sys.argv)
    w = Main_Window()
    w.show()
    sys.exit(app.exec_())
"""
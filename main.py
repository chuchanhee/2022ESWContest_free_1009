import sys, cv2
import time

from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, \
    QPushButton, QApplication, QFrame, QDialog, QLabel
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from threading import Thread as TH
from multiprocessing import Queue
import TCP
from TCP import drying_socket
from absl import app as app_2


prev_time = 0
class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    def run(self):
        cap = self.VideoCapture(0)
        while True:
            ret, img = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

    def VideoCapture(self, port):
        cap = cv2.VideoCapture(port)
        return cap

class MyApp(QMainWindow):
    def setImage(self, image):
        self.vidio_camera.setPixmap(QPixmap.fromImage(image))

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Video'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()


    def initUI(self) -> object:
        font = QFont('Black')
        font.setPointSize(16)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()


        # camera동영상
        self.vidio_camera= QLabel(self) #label to show face with ROIs
        self.vidio_camera.setGeometry(20,30,640,480)
        self.vidio_camera.setStyleSheet("background-color: #000000")

        # Camera 표시
        self.Camera1 = QLabel(self)  # label to show stable HR
        self.Camera1.setGeometry(30,510, 150, 50)
        self.Camera1.setFont(font)
        self.Camera1.setText("camera")
        self.Camera1.setStyleSheet("Color : red")  # 글자색 변환

        #self.pixmap = QPixmap('elderly1.jpg')
        #self.button = QPushButton(self)
        #self.button.setPixmap(self.pixmap)
        #self.label.setContentsMargins(1005, 210, 310, 210)
        #self.label.resize(self.pixmap.width(), self.pixmap.height())


        # 윈도우 설정
        self.setGeometry(500, 500, 400, 300)  # x, y, w, h
        self.setWindowTitle('QFrame Window')

        self.setFixedSize(650, 400)

        # 첫번째 큐프레임
        self.frame = QFrame(self)
        self.frame.setGeometry(800, 4, 160, 220)
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(2)
        self.frame.setMidLineWidth(2)

        # 두번째 큐프레임
        self.frame = QFrame(self)
        self.frame.setGeometry(1000, 4, 319, 220)
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setLineWidth(2)
        self.frame.setMidLineWidth(2)

        print(self.frame.frameWidth())

        # QLabel 에서 선택한 값 표시
        self.label = QLabel(self)
        self.label.setGeometry(1005, 290, 150, 30)
        self.label.setStyleSheet('background-color : #FFFFFF')

        # QRadioButton1 위젯 생성
        #self.radio1 = QRadioButton('측정실패', self)
        #self.radio1.clicked.connect(self.radio_select)
        #self.radio1.setGeometry(1005, 220, 150, 30)
        # QRadioButton2
        #self.radio2 = QRadioButton('측정완료', self)
        #self.radio2.clicked.connect(self.radio_select)
        #self.radio2.setGeometry(1005, 250, 150, 30)

        # QButton 위젯 생성
        self.button = QPushButton('새창', self)
        self.button.clicked.connect(self.nedialog_open)
        self.button.setGeometry(1005, 10, 308, 60)

        # QDialog 설정
        self.dialog = QDialog()

        # 스마트팩토리 초기화면 윈도우 설정
        self.setGeometry(300, 300, 500, 300)  # x, y, w, h
        self.setWindowTitle('SMART FACTORY')

        # 초기화면 실행버튼
        self.pb_toggled = QPushButton('연속 시작 버튼', self)
        self.pb_toggled.setGeometry(805, 10, 150, 30)
        self.pb_toggled.toggled.connect(self.change_toggled)
        self.pb_toggled.setCheckable(False)
        self.pb_toggled.toggle()

        # 초기화면 단속실행버튼
        self.pb_clicked = QPushButton('시작 버튼', self)
        self.pb_clicked.setGeometry(805, 70, 150, 30)
        self.pb_clicked.clicked.connect(self.button_clicked)
        self.pb_clicked.setText('단속 동작 버튼')

        # 초기화면 이벤트 발생 버튼(클릭 하는 순간 이벤트 발생)
        self.pb_pressed = QPushButton('비상 정지 버튼', self)
        self.pb_pressed.setGeometry(805, 130, 150, 30)
        self.pb_pressed.pressed.connect(self.button_pressed)

        # 초기화면 이벤트 발생 버튼(눌렀다가 떼는 순간 이벤트 발생)
        self.pb_released = QPushButton('정지 버튼', self)
        self.pb_released.setGeometry(805, 190, 150, 30)
        self.pb_released.released.connect(self.button_released)


        # 전체화면
        screen = QtWidgets.QDesktopWidget().screenGeometry()

        self.setWindowTitle('QPushButton')
        self.setGeometry(800, 600, screen.width(), screen.height())

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
            self.label.set지Text('이송공정 완료')
        elif self.radio2.isChecked():
            self.label.setText('전체공정 완료')





    # ComboBox 선택 이벤트
    def change_toggled(self):
        print('연속동작이 실행 되었습니다')
        drying_socket.write_contact.put(0x02)
    def button_clicked(self):
        print('단속동작이 실행 되었습니다')
        drying_socket.write_contact.put(0x03)
    def button_pressed(self):
        print('비상정지가 실행 되었습니다')

    def button_released(self):
        print('정지되었습니다')

    # Dialog 닫기 이벤트
    def dialog_close(self):
        self.dialog.close()



if __name__ == '__main__':
    q = Queue()
    #a = TCP.drying_socket.mobile_socket()

    #Process1= TH(target=a.mobile_bind,args=())
    #Process1.start()

    #d = drying_socket.PLC_Network()
    #print('성공')
    #Process2 = TH(target=d.PLC_Connect,args=())


   #Process2.start()

    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())



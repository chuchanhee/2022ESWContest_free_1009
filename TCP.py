from multiprocessing import Process,Queue,freeze_support
from threading import Thread
from socket import *
import time
import sys
sys.path.append('/C:/Users/Yun/Desktop/cont/rolypoly2/dxl_control/dxl_test.py')

from dxl_control import dxl_test
from dxl_control2 import dxl_test as dxl2


class drying_socket(): # 통신관련 함수들을 하나의 클래스에 묶음.
    que = "aaa"
    write_contact = Queue()
    read_que = Queue()
    msg2 = "bbb"

    class mobile_socket():  # 모바일 통신관련 클래스
        ip = '192.168.10.20'
        #ip = '192.168.43.219'
        port = 8080
        serverS = socket(AF_INET, SOCK_STREAM)  # ip,port 지정하고 소켓생성

        def __init__(self):

            pass

        def mobile_bind(self):
            self.serverS.bind((self.ip, self.port))        # 모바일 통신시 파이썬은 서버로 구동되기 때문에 클래스를 스레딩돌리면 알아서 서버로 바인딩함.
            self.serverS.listen(3)
            print('The server is ready to receive')
            client_Socket, addr = self.serverS.accept()  # 연결되면 데이터를 받는다.
            print('Accept!')
            try:
                while True:
                    data = client_Socket.recv(5)        # 따로 사용한 프로토콜이 없기때문에 바로 데이터를 받는다.
                    msg = data.decode()          # 수신된 데이터를 str형식으로 decode한다. msg의 데이터를 구분하여 응답

                    if msg[0] == 'a':
                        try:
                            read_thread = Thread(target = self.mobile_read, args =(client_Socket,))
                            read_thread.start()
                            read_thread.join()
                        except:
                            print('연결을 확인해주세요.')


                    elif msg[0] == 'b':
                        try:
                            write_thread = Thread(target = self.mobile_write, args=(client_Socket, msg))
                            write_thread.start()
                            write_thread.join()
                        except:
                            print("연결을 확인해주세요.")
                            return
                    else:
                        print("none")
                    # data = msg.encode()       #  데이터는 encode()를 이용하여 바이트(bytes)로 변환후 전송
            except:
                print("실패")                     # 접속이 끊기면 except발생


        def mobile_read(self, client_Socket):
            msg = drying_socket.que       # PLC로부터 읽어온 후 저장한 변수값을 읽어들임
            if msg != drying_socket.msg2:                       # queue값이 빈문자열이 아니라면 모바일로 전송
                data = msg.encode()
                client_Socket.sendall(data)
                drying_socket.msg2 = msg


        def mobile_write(self, client_Socket, msg):
            drying_socket.write_contact.put(int(msg[1:],16))
            data = msg.encode()
            client_Socket.sendall(data)


    class PLC_Network():    # PLC 통신관련 클래스

        IP = "192.168.10.40"
        PORT = 502
        PLC_socket = socket(AF_INET, SOCK_STREAM)  # ip,port 지정및 소켓생성
        def __init__(self):
            pass

        def PLC_Connect(self):
            try:
                self.PLC_socket.connect((self.IP,self.PORT))
                print("PLC connect success")
            except:
                print("PLC connect failed")
            thread2 = Thread(target=self.read_frame, args=())
            thread2.start()
            thread1 = Thread(target=self.write_frame, args=())
            thread1.start()
            thread1.join()
            thread2.join()

        def write_frame(self):                                      # 데이터 전송시 modbusTCP 프로토콜을 이용하여 데이터 전송
            while True:
                getque = drying_socket.write_contact.get()
                if getque != 0:
                    dummy1 = [0, 0, 0, 0, 0, 6, 1, 5, 0, 0, 0xff, 0]    # 프로토콜 전송 프레임을 default값으로 정해놓음.
                    dummy1[9] = getque                                # 함수 실행시 (접점, onn/off)를 받아 수행.
                    self.PLC_socket.send(bytes(dummy1))                 # 바이트(bytes)로 변환하여 데이터 전송
                    self.PLC_socket.recv(1024)                                   # 데이터 전송 후 데이터 수신준비
                    time.sleep(0.2)
                    dummy1[10] = 0
                    self.PLC_socket.send(bytes(dummy1))                    # 바이트(bytes)로 변환하여 데이터 전송
                    self.PLC_socket.recv(1024)

        def read_frame(self):                      # PLC로부터 정보를 읽어와 모니터링 기능을 수행한다. 0x00~0x38(56)까지
            dummy2 = [0, 0, 0, 0, 0, 6, 1, 1, 0, 0, 0, 0x20]    # ModBusTCP 프로토콜 프레임을 default값으로 정해놓음.
            recieve2 = ''
            Check = 0                                           # 값이 변경됨을 감지하면 그값을 Check에 넣음
            Check2 = 0
            while True:
                    self.PLC_socket.send(bytes(dummy2))             # ModBusTCP 프로토콜로 읽기 요청을 보냄.
                    recv = self.PLC_socket.recv(16)
                    recieve1 = recv.hex()[18:]                      # 응답받은 값중 필요한 값(18:)만 선별하여 확인함.
                    #####################print(recieve1)
                    if len(recieve2) == 0:
                        recieve2 = recv.hex()[18:]
                    if recieve1 != recieve2:

                        for i in range(0,len(recieve1),2):                         # for문을 돌려 변경된 값을 확인한다.
                            #   if int(recieve1[i],16) > int(recieve2[i],16):
                                recv1 = int(recieve1[i],16)# - int(recieve2[i],16)     # 데이터를 정수화하여 이전 데이터와 비교연산.
                                if recv1 == 1:                                              # 정수화 했을 시에 1,2,4,8에 해당하는 접점을 판별.
                                    Check = hex((i*4)+4)                                    # 16진수 값으로 # 1대 박진문이 넣은건데 안넣어도 문제 없을듯 #2대 윤진원 수정
                                elif recv1 == 2:
                                    Check = hex((i*4)+5)
                                elif recv1 == 4:
                                    Check = hex((i*4)+6)
                                elif recv1 == 8:
                                    Check = hex((i*4)+7)

                            #if int(recieve1[i + 1], 16) > int(recieve2[i + 1], 16):
                                recv2 = int(recieve1[i + 1], 16)# - int(recieve2[i + 1], 16)  # 한번에 두개씩 비교연산.
                                if recv2 == 1:
                                    Check = hex((i*4))
                                elif recv2 == 2:
                                    Check = hex((i*4)+1)
                                elif recv2 == 4:
                                    Check = hex((i*4)+2)
                                elif recv2 == 8:
                                    Check = hex((i*4)+3)
                    recieve2 = recieve1                                 # 다음 데이터 비교를 위해 recieve2에 데이터 저장
                    if Check2 != Check:
                        drying_socket.read_que.put(Check)                              # 변환이 감지된 값을 queue에 저장
                        drying_socket.que = Check                        # 변환이 감지된 값을 queue에 저장
                        Check2 = Check
                        print(Check)
                        if Check == hex(0x10):
                            th2 = Thread(target=dxl_test.RB2_POS1)
                            th2.start()
                        if Check == hex(0x11):
                            th3 = Thread(target=dxl_test.RB2_POS2)
                            th3.start()
                        if Check == hex(0xe):
                            th4 = Thread(target=dxl2.RB3_POS1)          #22.01.13 thread, 원래는 실행시 함수를 만나면 따로 실행하지만, 이 코딩은 같이 실행한다.
                            th4.start()

                    time.sleep(0.05)



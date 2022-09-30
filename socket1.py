import sys,cv2
from socket import *
from threading import Thread
from multiprocessing import Queue
from TCP import drying_socket

if __name__ == '__main__':
    q = Queue()
    a = drying_socket.mobile_socket()
    Process1 = Thread(target=a.mobile_bind, args=())
    Process1.start()

    d = drying_socket.PLC_Network()
    print('성공')
    Process2 = Thread(target=d.PLC_Connect, args = ())

    Process2.start()
    Process2.join()
#drying_socket.write_contact.put(0x01)
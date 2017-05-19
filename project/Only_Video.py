import cv2
import time
import numpy
import sys
from win32api import GetSystemMetrics
import thread
import os

WIDTH = GetSystemMetrics(0)
HEIGHT = GetSystemMetrics(1)
blank_image = numpy.zeros((500,600,3), numpy.uint8)
class Video:
    def __init__(self):
        #Video vars
        self.frame = None
        self.capture = None
        self.flag = False
    def Get_Self_Img(self,sock):
        self.capture = cv2.VideoCapture(0)
        while 1:
            # if needed to be closed
            self.If_user_exit()
            try:
                ret, self.frame = self.capture.read()
                cv2.imshow("Server_Self", self.frame)
            except:
                self.If_user_exit()
                self.frame = blank_image
                cv2.imshow("Server_Self", self.frame)
            cv2.resizeWindow("Server_Self", 600, HEIGHT/2)
            cv2.moveWindow("Server_Self", -15, HEIGHT/2)
            if cv2.waitKey(1) & 0xFF == ord('q'):
               pass
            self.Send_Video(sock)

    def Send_Video(self, sock):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, imgencode = cv2.imencode('.jpg', self.frame, encode_param)
        data = numpy.array(imgencode)
        stringData = data.tostring()
        try:
            sock.send(str(len(stringData)).ljust(16))
            sock.send(stringData)
        except:
            self.flag = True
        time.sleep(0.1)

    def recvall(self, sock, count):
        buf = b''
        while count:
            try:
                newbuf = sock.recv(count)
            except:
                self.flag = True
                break
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def Recv_Data(self,sock):
        data = 1
        while 1:
            #if needed to be closed
            self.If_user_exit()

            try:
                length = self.recvall(sock, 16)
                stringData = self.recvall(sock, int(length))
                data = numpy.fromstring(stringData, dtype='uint8')
                decimg = cv2.imdecode(data, 1)
                cv2.imshow('Server_Other', decimg)
            except:
                self.If_user_exit()
                decimg = blank_image    #img blank
                cv2.imshow('Server_Other', decimg)
            # cv2.moveWindow("Server_Other", -15, -23)
            cv2.resizeWindow("Server_Other", 600, HEIGHT/2)
            cv2.moveWindow("Server_Other", -15, 0)
            if cv2.waitKey(1) & 0xFF == ord('q'):
               pass

    def If_user_exit(self):
        if self.flag:
            thread.exit()

    def Close(self):
            self.capture.release()
            cv2.destroyAllWindows()

import cv2
import socket
import numpy
import time
import datetime
import multiprocessing

class Sock():
    def __init__(self):
        PORT = 5001
        IP = "0.0.0.0"
        #Socket vars
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((IP,PORT))
        s.listen(True)
        self.sock, addr = s.accept()
        #Video vars
        self.frame = None

    def Send_Video(self):

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, imgencode = cv2.imencode('.jpg', self.frame, encode_param)
        data = numpy.array(imgencode)
        stringData = data.tostring()
        self.sock.send(str(len(stringData)).ljust(16))
        self.sock.send(stringData)
        time.sleep(0.1)


    def Get_Self_Img(self):
        capture = cv2.VideoCapture(0)
        while 1:
        #capture video
            ret, self.frame = capture.read()
            cv2.imshow('frame',self.frame)
            cv2.moveWindow("frame",-15,528)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            self.Send_Video()


    def recvall(self,sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf


    def Recv_Data(self):
        data = 1
        while data != '':
            length = self.recvall(self.sock, 16)
            stringData = self.recvall(self.sock, int(length))
            data = numpy.fromstring(stringData, dtype='uint8')
            print datetime.datetime.now()

            decimg=cv2.imdecode(data,1)
            cv2.imshow('SERVER', decimg)
            cv2.moveWindow("SERVER",-15,-23)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.sock.close()

    def Main(self):

        SendProc = multiprocessing.Process(target=self.Get_Self_Img()).run()
        RecvProc = multiprocessing.Process(target=self.Recv_Data()).run()

        self.sock.close()
        # When everything done, release the capture
        self.capture.release()
        cv2.destroyAllWindows()

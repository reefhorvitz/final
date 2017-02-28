import cv2
import socket
import numpy
import time
class Sock():
    def __init__(self,ADD):
        #Socket vars
        self.sock = socket.socket()
        self.sock.connect(ADD)
        #Video vars
        self.capture = cv2.VideoCapture(0)
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
        self.capture = cv2.VideoCapture(0)
        while 1:
        #capture video
            ret, self.frame = self.capture.read()
            cv2.imshow('frame',self.frame)
            cv2.moveWindow("frame",-15,528)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            self.Send_Video()

    def Main(self):
        self.Get_Self_Img()
        self.sock.close()
        # When everything done, release the capture
        self.capture.release()
        cv2.destroyAllWindows()
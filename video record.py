import cv2
import socket
import numpy
import time
TCP_IP = '127.0.0.1'
TCP_PORT = 5001

sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))

capture = cv2.VideoCapture(0)
# for i in range(0, 30):
while 1:

    ret, frame = capture.read()


    cv2.imshow('frame',frame)
    cv2.moveWindow("frame",-15,528)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = numpy.array(imgencode)
    stringData = data.tostring()

    sock.send(str(len(stringData)).ljust(16))
    sock.send(stringData)

    time.sleep(0.1)

sock.close()
# When everything done, release the capture
capture.release()
cv2.destroyAllWindows()
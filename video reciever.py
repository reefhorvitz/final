import socket
import cv2
import datetime

def recvall(sock, count):
    buf = b''
    while count:x
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

TCP_IP = '0.0.0.0'
TCP_PORT = 5001
ADD = (TCP_IP,TCP_PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADD)
s.listen(True)
conn, addr = s.accept()
data = 1
while data != '':
    length = recvall(conn, 16)
    stringData = recvall(conn, int(length))
    data = numpy.fromstring(stringData, dtype='uint8')
    print datetime.datetime.now()

    decimg=cv2.imdecode(data,1)
    cv2.imshow('SERVER', decimg)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
s.close()
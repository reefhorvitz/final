import cv2
import time
import numpy
import sys

class Video:
	def __init__(self):
		#Video vars
		self.frame = None
		self.capture = None
		self.flag = False

	def Get_Self_Img(self,sock):
		self.capture = cv2.VideoCapture(0)
		while 1:
			try:
				ret, self.frame = self.capture.read()
				cv2.imshow("Server_Self", self.frame)
				cv2.moveWindow("Server_Self", -15, 528)
			except:
				self.flag = True
				return
			if cv2.waitKey(1) & 0xFF == ord('q'):
				# When everything done, release the capture
				self.capture.release()
				cv2.destroyAllWindows()
				sock.close()
				self.flag = True
				break
			self.Send_Video(sock)

	def Send_Video(self, sock):

		encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
		result, imgencode = cv2.imencode('.jpg', self.frame, encode_param)
		data = numpy.array(imgencode)
		stringData = data.tostring()
		sock.send(str(len(stringData)).ljust(16))
		sock.send(stringData)
		time.sleep(0.1)

	def recvall(self, sock, count):
		buf = b''
		while count:
			newbuf = sock.recv(count)
			if not newbuf: return None
			buf += newbuf
			count -= len(newbuf)
		return buf

	def Recv_Data(self,sock):
		data = 1
		while data != '':
			try:
				length = self.recvall(sock, 16)
				stringData = self.recvall(sock, int(length))
				data = numpy.fromstring(stringData, dtype='uint8')
				decimg = cv2.imdecode(data, 1)
				cv2.imshow('Server_Other', decimg)
				cv2.moveWindow("Server_Other", -15, -23)
			except:
				self.flag = True
				return
			if cv2.waitKey(1) & 0xFF == ord('q'):
				self.capture.release()
				cv2.destroyAllWindows()
				sock.close()
				self.flag = True
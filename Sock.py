import cv2
import socket
import numpy
import time
import datetime
import multiprocessing
import sys

class Server():
	def __init__(self):
		PORT = 5001
		IP = "0.0.0.0"
		ADD = (IP, PORT)
		#Socket vars
		s = socket.socket()
		s.bind(ADD)
		s.listen(1)
		self.sock, addr = s.accept()
		#Video vars
		self.frame = None
		self.capture = None


	def recvall(self, count):
		buf = b''
		while count:
			newbuf = self.sock.recv(count)
			if not newbuf: return None
			buf += newbuf
			count -= len(newbuf)
		return buf


	def Send_Video(self):

		encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
		result, imgencode = cv2.imencode('.jpg', self.frame, encode_param)
		data = numpy.array(imgencode)
		stringData = data.tostring()
		self.sock.send(str(len(stringData)).ljust(16))
		self.sock.send(stringData)
		time.sleep(0.1)


	def Recv_Data(self):
		data = 1
		while data != '':
			length = self.recvall(16)
			stringData = self.recvall(int(length))
			data = numpy.fromstring(stringData, dtype='uint8')
			print datetime.datetime.now()
			decimg = cv2.imdecode(data, 1)
			cv2.imshow('Server_Other', decimg)
			cv2.moveWindow("Server_Other", -15, -23)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		self.sock.close()


	def Get_Self_Img(self):
		self.capture = cv2.VideoCapture(0)
		while 1:
			ret, self.frame = self.capture.read()
			try:
				cv2.imshow("Server_Self", self.frame)
				cv2.moveWindow("Server_Self", -15, -23)
			except:
				pass
			if cv2.waitKey(1) & 0xFF == ord('q'):
				# When everything done, release the capture
				self.capture.release()
				cv2.destroyAllWindows()
				break
			self.Send_Video()

	def Exit(self, send, recv):
		while True:
			if not (send.is_alive() and recv.is_alive()):   #if one of them has been terminated
				send.terminate()
				recv.terminate()
				self.sock.close()
				self.s.close()

				sys.exit(0)


	def Main(self):

		SelfProc = multiprocessing.Process(target=self.Get_Self_Img())
		SelfProc.run()
		RecvProc = multiprocessing.Process(target=self.Recv_Data())
		RecvProc.run()
		self.Exit(SelfProc, RecvProc)



class Client():
	def __init__(self, ADD):
		#Socket vars
		self.sock = socket.socket()
		self.sock.connect(ADD)
		#Video vars
		self.frame = None
		self.capture = None

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
			try:
				cv2.imshow('Client_Self', self.frame)
				cv2.moveWindow("Client_Self", -15, 528)
			except:
				pass
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			self.Send_Video()


	def recvall(self, count):
		buf = b''
		while count:
			newbuf = self.sock.recv(count)
			if not newbuf: return None
			buf += newbuf
			count -= len(newbuf)
		return buf


	def Recv_Data(self):
		data = 1
		while data != '':
			length = self.recvall(16)
			stringData = self.recvall(int(length))
			data = numpy.fromstring(stringData, dtype='uint8')
			print datetime.datetime.now()

			decimg = cv2.imdecode(data, 1)
			cv2.imshow('Client_Other', decimg)
			cv2.moveWindow("Client_Other", -15, -23)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				# When everything done, release the capture
				self.capture.release()
				cv2.destroyAllWindows()
				break
		self.sock.close()

	def Exit(self, send, recv):
		while True:
			if not (send.is_alive() and recv.is_alive()):   #if one of them has been terminated
				send.terminate()
				recv.terminate()
				self.sock.close()
				sys.exit(0)

	def Main(self):

		SelfProc = multiprocessing.Process(target=self.Get_Self_Img())
		SelfProc.run()
		RecvProc = multiprocessing.Process(target=self.Recv_Data())
		RecvProc.run()
		self.Exit(SelfProc, RecvProc)
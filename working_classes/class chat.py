import socket
class chat():
	def __init__(self,sock):
		self.s = sock

	def recv_msg(self):
		while True:
			print self.s.recv(1024)

	def send_msg(self):
		while True:
			data = raw_input()
			self.s.send(data)
import socket
import Tkinter

class Chat():

	def recv_msg(self,s):
		while True:
			print s.recv(1024)

	def send_msg(self,s):
		while True:
			data = raw_input()
			s.send(data)
import socket
from Tkinter import *

class Chat():

	def __init__(self):
		self.root = Tk()
		self.myentery = Entry(self.root)
		self.myentery.pack(side = BOTTOM)
		self.chattext = Text(self.root)
		self.sendbutton = Button(self.root,text = "SEND" , command = self.pressed)
		self.is_pressed = False

	def pressed(self):
		self.is_pressed = True

	def recv_msg(self,s):
		while True:
			data = s.recv(1024)
			if data:
				self.chattext.insert(END,"HIM : "+data)

	def send_msg(self,s):
		if self.is_pressed:
			msg = self.myentery.get()
			s.send(msg)
			self.chattext.insert(END,"ME : "+msg)
			self.is_pressed = False

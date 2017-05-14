import socket
from Tkinter import *
import threading

class Chat():

	def __init__(self):
		self.root = Tk()
		self.root.attributes("-fullscreen", True)
		self.myentery = Entry(self.root)
		self.myentery.pack(side = BOTTOM)
		self.chattext = Text(self.root)
		self.chattext.pack(side = TOP)
		self.sendbutton = Button(self.root,text = "SEND" , command = self.pressed)
		self.sendbutton.pack(side = RIGHT)
		self.is_pressed = False

		#for the main loop
		thread = threading.Thread(target=self.mainloop)
		thread.start()

	def pressed(self):
		self.is_pressed = True

	def recv_msg(self,s):
		while True:
			data = s.recv(1024)
			if data:
				self.chattext.insert(END,"HIM : "+data+"\n")

	def send_msg(self,s):
		while True:
			if self.is_pressed:
				msg = self.myentery.get()
				s.send(msg)
				self.chattext.insert(END,"ME : "+msg+"\n")
				self.is_pressed = False
				self.myentery.delete(0,END)

	def mainloop(self):
		self.root.mainloop()
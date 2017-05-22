import os
import socket
from Tkinter import *
import threading
from win32api import GetSystemMetrics
import thread
WIDTH = GetSystemMetrics(0)
HEIGHT = GetSystemMetrics(1)

class Chat():

    def __init__(self):
        self.root = Tk()
        self.flag = False
        self.root.geometry('%dx%d+%d+%d'%(WIDTH/4, HEIGHT/2, 600, 0))
        self.root["bg"] = "#f2ea54"
        self.root.bind("<Return>",self.pressed)
        self.root.protocol("WM_DELETE_WINDOW", self.onexit)

        lableimage = Label(self.root,text = "Chat Locate", font = "34")
        lableimage.pack()

        self.chattext = Text(self.root, font = 28)
        self.chattext.config(stat = DISABLED)
        self.chattext.pack(fill = X)

        frame = Frame(self.root,height = 20)
        frame.pack()

        self.myentery = Entry(self.root)
        self.myentery.pack(fill  = X)

        self.sendbutton = Button(self.root,text = "SEND" , command = self.pressed)
        self.sendbutton.pack()

        self.is_pressed = False

        #for the main loop
        thread = threading.Thread(target=self.mainloop)
        thread.start()

    def pressed(self,ret = None):
        self.is_pressed = True

    def recv_msg(self,s):
        while True:
            if self.flag:
                self.onexit()
            try:
                data = s.recv(1024)
                if data == "#EXIT#":
                    self.flag = True
                    self.onexit()
            except:
                self.flag = True
                break
            if data :
                self.chattext.config(stat=NORMAL)
                self.chattext.insert(END,"HIM : "+data+"\n")
                self.chattext.config(stat=DISABLED)
            else:
                self.flag = True
                self.onexit()

    def send_msg(self,s):
        self.s = s
        while True:
            if self.flag:
                self.onexit()
            if self.is_pressed:
                msg = self.myentery.get()
                s.send(msg)
                self.chattext.config(stat=NORMAL)
                self.chattext.insert(END,"ME : "+msg+"\n")
                self.chattext.config(stat=DISABLED)
                self.is_pressed = False
                self.myentery.delete(0,END)

    def onexit(self, key = None):
        try:
            self.s.send("#EXIT#")
            self.flag = True
        except:
            pass
        thread.exit()

    def Close(self):
        self.root.quit()

    def mainloop(self):
       self.root.mainloop()
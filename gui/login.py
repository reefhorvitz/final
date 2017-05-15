from Tkinter import *
import sys
import socket
import subprocess

class main_frame:
    def __init__(self,root):
        root.title("ChatLocate")
        root.bind('<Return>', self.server_con)
        root["bg"] = "#f2ea54"
        self.logo = PhotoImage(file="mylogo.gif")
        logolab = Label(root, image=self.logo, bg=root["bg"])
        logolab.grid(columnspan = 2)

        namelabel = Label(root,text = "Enter your full phone number:",font = 30,bg = root["bg"])
        namelabel.grid()
        self.phoneentery = Entry(root)
        self.phoneentery.grid(row = 1,column=1,sticky = W)

        button = Button(root,text = "Submit",command = self.server_con)
        button.grid(row=2,columnspan = 2)

    def server_con(self,key = None):
        ip = "127.0.0.1"
        PORT =5004
        ADD = (ip,PORT)
        sock = socket.socket()
        sock.connect(ADD)
        sock.send("phone-"+self.phoneentery.get())
        data = sock.recv(1024)
        if data.startswith("client"):
            process = subprocess.Popen(['client.py', data[7:]], shell=True, stderr=subprocess.STDOUT,
                                       stdout=subprocess.PIPE)

        else:
            process = subprocess.Popen('server.py', shell=True, stderr=subprocess.STDOUT,
                                       stdout=subprocess.PIPE)
        print process.communicate()[0][:-2]
root = Tk()
mainroot = main_frame(root)
root.mainloop()
from Tkinter import *
import sys
import socket
import subprocess

class main_frame:
    def __init__(self,root):
        self.root = root
        self.root.title("ChatLocate")
        self.root.bind('<Return>', self.server_con)
        self.root["bg"] = "#f2ea54"
        self.logo = PhotoImage(file="mylogo.gif")
        logolab = Label(self.root, image=self.logo, bg=self.root["bg"])
        logolab.grid(columnspan = 2)

        self.namelabel = Label(self.root,text = "Enter your Email :",font = 30,bg = self.root["bg"])
        self.namelabel.grid()
        self.phoneentery = Entry(self.root)
        self.phoneentery.grid(row = 1,column=1,sticky = W)

        self.button = Button(root,text = "Submit",command = self.server_con)
        self.button.grid(row=2,columnspan = 2)

    def server_con(self,key = None):
        ip = "127.0.0.1"
        PORT =5004
        ADD = (ip,PORT)
        sock = socket.socket()
        sock.connect(ADD)
        sock.send("phone-"+self.phoneentery.get())
        self.help_num(sock)

    def help_num(self,sock):
        self.namelabel['text'] = "Enter verification number :"
        self.button.configure(text = "Submit", command = lambda: self.num_ver(sock))
        self.root.bind("<Return>",self.num_ver)

    def num_ver(self,sock, key = None):
        sock.send("num-"+self.phoneentery.get())
        self.prog(sock)

    def prog(self,sock):
        data = sock.recv(1024)
        if data.startswith("client"):
            process = subprocess.call(['python','client.py', data[7:]], shell=True, stderr=subprocess.STDOUT,
                                       stdout=subprocess.PIPE)

        else:
            process = subprocess.call(['python','server.py'], shell=True, stderr=subprocess.STDOUT,
                                       stdout=subprocess.PIPE)
        print process.communicate()[0][:-2]
root = Tk()
mainroot = main_frame(root)
root.mainloop()
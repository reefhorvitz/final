from Tkinter import *
import sys
import socket
import subprocess
from threading import Thread

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
        self.sock = None
        self.flag = False

    def server_con(self,key = None):
        try:
            ip = sys.argv[1]
        except:
            ip = "10.0.0.3"
        PORT =5004
        ADD = (ip,PORT)
        self.sock = socket.socket()
        self.sock.connect(ADD)
        self.sock.send("phone-"+self.phoneentery.get())
        self.help_num()

    def help_num(self):
        self.phoneentery.delete(0,END)
        self.namelabel['text'] = "Enter verification number :"
        self.button.configure(text = "Submit", command = self.num_ver)
        self.root.bind("<Return>", self.num_ver)

    def num_ver(self, key = None):
        self.sock.send("num-"+self.phoneentery.get())
        self.prog(self.sock)

    def prog(self,sock):
        self.root.unbind("<Return>")
        self.phoneentery.destroy()
        self.button.destroy()
        self.namelabel['text'] = "PLEASE WAIT !!!"
        self.flag = True

    def Create_con(self):
            while True:
                if self.flag:
                    try:
                         data = self.sock.recv(1024)
                         print data
                         break
                    except:
                        pass
            try:
                self.root.destroy()
                if data.startswith("client"):
                    process = subprocess.call(['python','client.py', data[7:]], shell=True, stderr=subprocess.STDOUT,
                                               stdout=subprocess.PIPE)
                    print "process started"

                else:
                    process = subprocess.call(['python','server.py'], shell=True, stderr=subprocess.STDOUT,
                                               stdout=subprocess.PIPE)
            except:
                    print "Connection Lost"
root = Tk()
mainroot = main_frame(root)
Connection_Thread = Thread(target=mainroot.Create_con)
Connection_Thread.start()
root.mainloop()

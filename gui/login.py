from Tkinter import *
import sys
import socket

class main_frame:
    def __init__(self,root):
        root.title("ChatLocate")
        root.bind('<Return>', self.OnEnter)
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

    def OnEnter(self,a):
        sys.exit(0)

    def server_con(self):
        ip = "127.0.0.1"
        PORT =5004
        ADD = (ip,PORT)
        sock = socket.socket()
        sock.connect(ADD)
        sock.send("phone-"+self.phoneentery.get())


root = Tk()
mainroot = main_frame(root)
root.mainloop()
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
        ip = "10.0.0.18"
        PORT =5004
        ADD = (ip,PORT)
        sock = socket.socket()
        sock.connect(ADD)
        sock.send("phone-"+self.phoneentery.get())
        self.help_num(sock)

    def help_num(self,sock):
        self.phoneentery.delete(0,END)
        self.namelabel['text'] = "Enter verification number :"
        self.button.configure(text = "Submit", command = lambda: self.num_ver(sock))
        self.root.bind("<Return>", lambda a: self.num_ver(sock))

    def num_ver(self,sock, key = None):
        sock.send("num-"+self.phoneentery.get())
        self.prog(sock)

    def prog(self,sock):
        self.root.unbind("<Return>")
        self.phoneentery.pack_forget()
        self.button.pack_forget()
        self.namelabel['text'] = "PLEASE WAIT !!!"
        self.Create_con(sock)

    def Create_con(self,sock):
        while True:
            try:
                 data = sock.recv(1024)
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
root.mainloop()
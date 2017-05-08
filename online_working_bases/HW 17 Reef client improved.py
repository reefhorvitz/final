import socket
import msvcrt
import select
import time
import sys
import re
def color(string, status, bold):
    attr = []
    if status:
        # green
        attr.append('32')
    else:
        # red
        attr.append('31')
    if bold:
        attr.append('1')
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)
while True:
    name = raw_input("Enter Your Name(For instruction's type (help)):")
    if name.startswith("@"):
       print "Bad Name"
    if name == "help":
        print "For private massage type (! To (Name Of The User) (massage))"
        print "To get managers list type (view-managers)"
        print "if you are manager you can mute someone by typing (Mute=(Name of the user))"
        print "if you want to exit type (quit)"
        print "if you are manager you can turn other user to manager by typing (Turn M=(name of the user))"
        print "if you are manager you can kick someone from the chat by typing (kick=(name of the user))"
        print  "To get a list of the names in the server's list type(view-names)"
    else:
        break
IP = "127.0.0.1"
PORT = 1075
ADDR = (IP, PORT)
my_socket = socket.socket()
my_socket.connect(ADDR)
Open_Client_Socket = []
messages_to_send = []
def send_waiting_messages(wlist,name):
 for message in messages_to_send:
    if my_socket in wlist:
        sendMessage = message[0] +"#LenName="+str(len(name))+"#Name="+name+"#Option=1"+"#Time="+message[1]
        my_socket.send(sendMessage)
    if message[0]=="quit":
        sys.exit(0)
    messages_to_send.remove(message)
def read_waiting_messages(rlist):
 if my_socket in rlist:
    return my_socket.recv(1024)
print "Enter:",
message = ""
while True:
    rlist,wlist,xlist = select.select([my_socket]+Open_Client_Socket,[my_socket]+Open_Client_Socket,[])
    if not my_socket in wlist:
        my_socket.close()
        sys.exit(0)
    if msvcrt.kbhit():
        ch = msvcrt.getche()
        if ch == "\b":
            if message != "":
                message = message[:-1]
                sys.stdout.write(" ")
                sys.stdout.write("\b")
            else:
                sys.stdout.write(":")
        elif ch=="\r" :
            if message == "":
                print
                print "Enter:",
                continue
            if message.startswith("!"):
                lstmsg = message.split(" ")
                othername = lstmsg[lstmsg.index("To")+1]
                message = "! "+str(len(othername))+message[1:]
            TimeOfMessage = time.strftime("%H:%M",time.localtime())
            messages_to_send.append((message,TimeOfMessage))
            sys.stdout.write("\b")
            print color("At "+TimeOfMessage+" You: ",1,1),
            print message
            message  = ""
            print "Enter:",
        else:
            message += ch
    send_waiting_messages(wlist,name)
    data = read_waiting_messages(rlist)
    if(data):
        sys.stdout.write("\r")
        match = re.search("(At.+From.+: )(.+)",data)
        if match:
            print color(match.group(1),0,1),
            print match.group(2)
        else:
            print data
        print "Enter:"+message,
my_socket.close()
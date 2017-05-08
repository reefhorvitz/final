import socket
import select
import re
IP = "0.0.0.0"
PORT = 1075
ADRR = (IP,PORT)
server_socket = socket.socket()
server_socket.bind(ADRR)
server_socket.listen(5)
Open_Client_Socket = []
messages_to_send = []
def send_waiting_messages(wlist):
 for message in messages_to_send:
    (client_socket, data) = message
    if client_socket in wlist:
        client_socket.send(data)
    messages_to_send.remove(message)
ListOfManagers = ["reef"]
MuteList = []
NameToSocket = {}
while True:
    rlist, wlist, xlist = select.select([server_socket] + Open_Client_Socket, Open_Client_Socket, [])
    for current_socket in rlist:

        if current_socket is server_socket:
            (new_socket, address) = server_socket.accept()
            Open_Client_Socket.append(new_socket)
        else:
            try:
                data = current_socket.recv(1024)
                print "Got Data : "+ data
                match = re.search("(.+)#LenName=(\d+)#Name=(.+)#Option=(\d)#Time=(.+)",data)
                message = str(match.group(1))
                LenOfName = int(match.group(2))
                name = str(match.group(3))
                option = int(match.group(4))
                timeofsend = str(match.group(5))
                if not name in NameToSocket:
                    NameToSocket[name] = current_socket
                if message=="quit":
                    a = int("a")
                if name in ListOfManagers:
                    name = "@"+name
                    if message.startswith("Turn M="):
                        ListOfManagers.append(message[7:])
                        continue
                    if message.startswith("Mute="):
                        MuteList.append(message[5:])
                        continue
                    if message.startswith("Kick="):
                        othername = message[5:]
                        Open_Client_Socket.remove(NameToSocket[othername])
                        NameToSocket[othername].close()
                        rlist,newlst,xlist = select.select([], Open_Client_Socket, [])
                        newlst.remove(current_socket)
                        for a in newlst:
                            messages_to_send.append((a,(timeofsend+" "+othername+" Has been kicked out of the chat")))
                        continue
                if message.startswith("view-managers"):
                    messages_to_send.append((current_socket,str(ListOfManagers)))
                    continue
                if message.startswith("view-names"):
                     messages_to_send.append((current_socket,str(NameToSocket.keys())))
                     continue
                elif name in MuteList:
                    messages_to_send.append((current_socket, "You Cannot Speak Here"))
                    continue
                elif message.startswith("!"):
                    match = re.search("! (\d) To (.+)$",message)
                    namelen = int(match.group(1))
                    privatemessage = match.group(2)
                    privatemessage = privatemessage[namelen:]
                    privatemessage = "Private From "+name+": "+privatemessage
                    othername = message[7:7+namelen]
                    messages_to_send.append((NameToSocket[othername],privatemessage))
                    continue
                CompleteMessage = "At "+timeofsend+" From "+name+": "+message
                for a in wlist:
                    if a != current_socket:
                        messages_to_send.append((a, CompleteMessage))
            except:
               current_socket.close()
               Open_Client_Socket.remove(current_socket)
               print "Connection with client closed."
               for a in wlist:
                    if a != current_socket:
                        messages_to_send.append((a,"At "+timeofsend+" "+name+" left the chat"))
    send_waiting_messages(wlist)

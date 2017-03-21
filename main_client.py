import  Sock
PORT = 5001
IP = "127.0.0.1"
ADD = (IP,PORT)
sock = Sock.Client(ADD)
sock.Main()
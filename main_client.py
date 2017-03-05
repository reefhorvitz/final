import  class_client
PORT = 5001
IP = "127.0.0.1"
ADD = (IP,PORT)
sock = class_client.Sock(ADD)
sock.Main()
import socket
import Only_Video
import threading
import sys
import time

def Sock_Connect():
	PORT1 = 5001
	PORT2 = 5002
	IP = "192.168.30.20"
	s1 = socket.socket()
	s2 = socket.socket()
	s1.connect((IP, PORT1))
	s2.connect((IP, PORT2))
	return (s1,s2)

send, recv = Sock_Connect()
base = Only_Video.Video()
base2 = Only_Video.Video()

def Exit(P1,P2,send,recv):
	while True:
		if not(P1.is_alive() and P2.is_alive()):
			P1.Terminate()
			P2.Terminate()
			send.close()
			recv.close()
			sys.exit(0)
		time.sleep(0.5)

Send_Thread = threading.Thread(target=base.Get_Self_Img,args=(send,))
Recv_Thread = threading.Thread(target=base2.Recv_Data,args=(recv,))
Send_Thread.start()
Recv_Thread.start()

Exit(Send_Thread,Recv_Thread,send,recv)


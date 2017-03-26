import socket
import Only_Video
import multiprocessing
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

def Exit(P1,P2,send,recv):
	while True:
		if not(P1.is_alive() and P2.is_alive()):
			P1.Terminate()
			P2.Terminate()
			send.close()
			recv.close()
			sys.exit(0)
		time.sleep(0.5)

Proc_Send = multiprocessing.Process(target=base.Get_Self_Img,args=(send,))
Proc_Recv = multiprocessing.Process(target=base.Recv_Data,args=(recv,))
Proc_Send.run()
Proc_Recv.run()

Exit(Proc_Recv,Proc_Send,send,recv)


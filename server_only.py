import socket
import Only_Video
import multiprocessing
import sys
import time

def Sock_Connect():
	PORT1 = 5001
	PORT2 = 5002
	IP = "0.0.0.0"
	#Socket vars
	s1 = socket.socket()
	s2 = socket.socket()
	s1.bind((IP,PORT1))
	s2.bind((IP,PORT2))
	s1.listen(1)
	s2.listen(1)
	recv_sock, addr = s1.accept()
	send_sock, addr = s2.accept()
	return (send_sock,recv_sock)

def Exit(P1,P2,send,recv):
	while True:
		if not(P1.is_alive() and P2.is_alive()):
			P1.Terminate()
			P2.Terminate()
			send.close()
			recv.close()
			sys.exit(0)
		time.sleep(0.5)

send, recv = Sock_Connect()
base = Only_Video.Video()

Proc_Send = multiprocessing.Process(target=base.Get_Self_Img, args=(send,))
Proc_Recv = multiprocessing.Process(target=base.Recv_Data, args=(recv,))
Proc_Send.run()
Proc_Recv.run()
Exit(Proc_Recv, Proc_Send, send, recv)

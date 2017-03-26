import socket
import Only_Video
import threading
import sys
import time

def Sock_Connect():
	PORT1 = 5002
	PORT2 = 5001

	IP = "0.0.0.0"
	#Socket vars
	s1 = socket.socket()
	s2 = socket.socket()

	s1.bind((IP,PORT1))
	s2.bind((IP,PORT2))

	s1.listen(1)
	s2.listen(1)

	send_sock, addr = s1.accept()
	recv_sock, addr = s2.accept()
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

Send_Thread = threading.Thread(target=base.Get_Self_Img, args=(send,))
Recv_Thread = threading.Thread(target=base.Recv_Data, args=(recv,))
Send_Thread.run()
Recv_Thread.run()
Exit(Recv_Thread, Send_Thread, send, recv)

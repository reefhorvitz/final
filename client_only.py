import socket
import Only_Video
import multiprocessing

def Sock_Connect():
	PORT1 = 5001
	PORT2 = 5002
	IP = "127.0.0.1"
	s1 = socket.socket()
	s2 = socket.socket()
	s1.connect((IP,PORT1))
	s2.connect((IP,PORT2))
	return (s1,s2)
send, recv = Sock_Connect()
base = Only_Video.Video()

Proc_Send = multiprocessing.Process(target=base.Get_Self_Img,args=(send,))
Proc_Recv = multiprocessing.Process(target=base.Recv_Data,args=(recv,))
Proc_Send.run()
Proc_Recv.run()



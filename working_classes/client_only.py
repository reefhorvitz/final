import socket
import Only_Video
import sound_class
import threading
import sys
import time

def Sock_Connect():
	PORT1 = 5001
	PORT2 = 5002
	PORT3 = 5003
	PORT4 = 5004

	IP = "192.168.30.29"

	s1 = socket.socket()
	s2 = socket.socket()
	s3 = socket.socket()
	s4 = socket.socket()

	s1.connect((IP, PORT1))
	s2.connect((IP, PORT2))
	s3.connect((IP, PORT3))
	s4.connect((IP, PORT4))

	return (s1, s2, s3, s4)

#varaibles for sock and functions
send_vid, recv_vid, send_aud, recv_aud = Sock_Connect()
base = Only_Video.Video()
base2 = Only_Video.Video()

audio = sound_class.OnlyAudio(send_aud)
audio2 = sound_class.OnlyAudio(recv_aud)

def Exit(P1,P2,P3,P4,s1,s2,s3,s4):
	while True:
		if not(P1.is_alive() and P2.is_alive()):
			#close proc
			P1.join()
			P2.join()
			P3.join()
			P4.join()
			#close sock
			s1.close()
			s2.close()
			s3.close()
			s4.close()

			sys.exit(0)
		time.sleep(0.5)

Send_Vid_Thread = threading.Thread(target=base.Get_Self_Img,args=(send_vid,))
Recv_Vid_Thread = threading.Thread(target=base2.Recv_Data,args=(recv_vid,))
Send_Aud_Thread = threading.Thread(target=audio.Send_Sound)
Recv_Aud_Thread = threading.Thread(target=audio2.Get_Sound)

Send_Vid_Thread.start()
Recv_Vid_Thread.start()
Send_Aud_Thread.start()
Recv_Aud_Thread.start()

Exit(Send_Vid_Thread, Recv_Vid_Thread, Send_Aud_Thread, Recv_Aud_Thread, send_aud, recv_aud, send_vid, recv_vid)
import socket
import Only_Video
import sound_class
import class_chat
import threading
import sys
import time

def Sock_Connect():
	PORT1 = 5001
	PORT2 = 5002
	PORT3 = 5003
	PORT4 = 5004
	PORT5 = 5005
	PORT6 = 5006

	IP = "192.168.30.29"

	s1 = socket.socket()
	s2 = socket.socket()
	s3 = socket.socket()
	s4 = socket.socket()
	s5 = socket.socket()
	s6 = socket.socket()

	s1.connect((IP, PORT1))
	s2.connect((IP, PORT2))
	s3.connect((IP, PORT3))
	s4.connect((IP, PORT4))
	s5.connect((IP, PORT5))
	s6.connect((IP, PORT6))

	return (s1, s2, s3, s4, s5, s6)


def Exit(base,s1,s2,s3,s4,s5,s6):
	while True:
		if base.flag:
			#close sock
			s1.close()
			s2.close()
			s3.close()
			s4.close()
			s5.close()
			s6.close()
			sys.exit(0)
		time.sleep(0.5)

#varaibles for sock and functions
send_vid, recv_vid, send_aud, recv_aud, send_chat, recv_chat = Sock_Connect()
base = Only_Video.Video()

audio = sound_class.OnlyAudio(send_aud)
audio2 = sound_class.OnlyAudio(recv_aud)
chat =  class_chat.Chat()



Send_Vid_Thread = threading.Thread(target=base.Get_Self_Img,args=(send_vid,))
Recv_Vid_Thread = threading.Thread(target=base.Recv_Data,args=(recv_vid,))
Send_Aud_Thread = threading.Thread(target=audio.Send_Sound)
Recv_Aud_Thread = threading.Thread(target=audio2.Get_Sound)
Send_Chat_Thread = threading.Thread(target=chat.send_msg, args=(send_chat,))
Recv_Chat_Thread = threading.Thread(target=chat.recv_msg, args=(recv_chat,))


Send_Vid_Thread.start()
Recv_Vid_Thread.start()
Send_Aud_Thread.start()
Recv_Aud_Thread.start()
Send_Chat_Thread.start()
Recv_Chat_Thread.start()

Exit(base, send_aud, recv_aud, send_vid, recv_vid, send_chat, recv_chat)
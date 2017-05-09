import socket
import sound_class
import threading
PORT1 = 5001
PORT2 = 5002
IP = "192.168.30.29"
s1 = socket.socket()
s2 = socket.socket()
s1.connect((IP, PORT1))
s2.connect((IP, PORT2))

audio = sound_class.OnlyAudio(s1)
audio2 = sound_class.OnlyAudio(s2)
Send_Aud_Thread = threading.Thread(target=audio.Send_Sound)
Recv_Aud_Thread = threading.Thread(target=audio2.Get_Sound)
Send_Aud_Thread.start()
Recv_Aud_Thread.start()

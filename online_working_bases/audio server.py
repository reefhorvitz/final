import socket
import sound_class
import threading

PORT1 = 5002
PORT2 = 5001
IP = "0.0.0.0"

s1 = socket.socket()
s2 = socket.socket()

s1.bind((IP, PORT1))
s2.bind((IP, PORT2))

s1.listen(1)
s2.listen(1)

send, addr = s1.accept()
recv, addr = s2.accept()

audio = sound_class.OnlyAudio(send)
audio2 = sound_class.OnlyAudio(recv)

Send_Aud_Thread = threading.Thread(target=audio.Send_Sound)
Recv_Aud_Thread = threading.Thread(target=audio2.Get_Sound)
Send_Aud_Thread.start()
Recv_Aud_Thread.start()
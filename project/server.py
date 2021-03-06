import socket
import Only_Video
import sound_class
import class_chat
import threading
import sys
import time

def Sock_Connect():
    PORT1 = 5002
    PORT2 = 5001
    PORT3 = 5004
    PORT4 = 5003
    PORT5 = 5006
    PORT6 = 5005


    IP = "0.0.0.0"

    #Socket vars
    s1 = socket.socket()
    s2 = socket.socket()
    s3 = socket.socket()
    s4 = socket.socket()
    s5 = socket.socket()
    s6 = socket.socket()

    s1.bind((IP, PORT1))
    s2.bind((IP, PORT2))
    s3.bind((IP, PORT3))
    s4.bind((IP, PORT4))
    s5.bind((IP, PORT5))
    s6.bind((IP, PORT6))


    s1.listen(1)
    s2.listen(1)
    s3.listen(1)
    s4.listen(1)
    s5.listen(1)
    s6.listen(1)

    send_vid, addr = s1.accept()
    recv_vid, addr = s2.accept()
    send_aud, addr = s3.accept()
    recv_aud, addr = s4.accept()
    send_chat, addr = s5.accept()
    recv_chat, addr = s6.accept()

    return (send_vid, recv_vid, send_aud, recv_aud, send_chat, recv_chat)


def Exit(base,chat,aud,s1,s2,s3,s4,s5,s6):
    while True:
        if chat.flag:
            chat.Close()
            aud.flag = True
            aud.Close()
            base.flag = True
            base.Close()

            #close sock
            s1.close()
            s2.close()
            s3.close()
            s4.close()
            s5.close()
            s6.close()
            print "pass"
            sys.exit(0)
        time.sleep(0.5)

if __name__ == "__main__":
    send_vid, recv_vid, send_aud, recv_aud, send_chat, recv_chat = Sock_Connect()
    base = Only_Video.Video()

    audio = sound_class.OnlyAudio()

    chat =  class_chat.Chat()
    tlist = []

    Send_Vid_Thread = threading.Thread(target=base.Get_Self_Img, args=(send_vid,))
    Recv_Vid_Thread = threading.Thread(target=base.Recv_Data, args=(recv_vid,))
    Send_Aud_Thread = threading.Thread(target=audio.Send_Sound, args=(send_aud,))
    Recv_Aud_Thread = threading.Thread(target=audio.Get_Sound, args=(recv_aud,))
    Send_Chat_Thread = threading.Thread(target=chat.send_msg, args=(send_chat,))
    Recv_Chat_Thread = threading.Thread(target=chat.recv_msg, args=(recv_chat,))

    Send_Vid_Thread.start()
    Recv_Vid_Thread.start()
    Send_Aud_Thread.start()
    Recv_Aud_Thread.start()
    Send_Chat_Thread.start()
    Recv_Chat_Thread.start()
    Exit(base, chat, audio, send_aud, recv_aud, send_vid, recv_vid, send_chat, recv_chat)

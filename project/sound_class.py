import socket
import pyaudio
import wave
import thread

class OnlyAudio:
    def __init__(self):
        #record
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.RECORD_SECONDS = 40
        self.WIDTH = 2
        self.p = pyaudio.PyAudio()
        self.flag = False

    def Send_Sound(self,s):
        try:
            self.stream1 = self.p.open(format=self.FORMAT,
                                      channels=self.CHANNELS,
                                      rate=self.RATE,
                                      input=True,
                                      frames_per_buffer=self.CHUNK)
            while True:
                frames = []
                for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
                    self.Exit()
                    data = self.stream1.read(self.CHUNK)
                    frames.append(data)
                    s.sendall(data)
        except:
            self.flag = True
            self.Exit()


    def Exit(self):
        if self.flag :
            thread.exit()

    def Close(self):
            self.stream1.stop_stream()
            self.stream1.close()
            self.stream2.stop_stream()
            self.stream2.close()
            self.p.terminate()

    def Get_Sound(self,s):
        try:
            self.stream2 = self.p.open(format=self.p.get_format_from_width(self.WIDTH),
                                      channels=self.CHANNELS,
                                      rate=self.RATE,
                                      output=True,
                                      frames_per_buffer=self.CHUNK)
            data = s.recv(1024)
            frames = []
            while data != '':
                self.Exit()
                self.stream2.write(data)
                data = s.recv(1024)
                frames.append(data)
        except:
            self.flag = True
            self.Exit()
        self.flag = True
        self.Exit()
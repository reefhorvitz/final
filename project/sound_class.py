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
        self.stream1 = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK)
        while True:
            self.Exit()
            frames = []
            for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
                try:
                    data = self.stream1.read(self.CHUNK)
                    frames.append(data)
                    s.sendall(data)
                except:
                    self.flag = True
                    break

    def Exit(self):
        if self.flag:
            self.stream1.stop_stream()
            self.stream1.close()
            self.stream2.stop_stream()
            self.stream2.close()
            self.p.terminate()
            thread.exit()

    def Get_Sound(self,s):
        self.stream2 = self.p.open(format=self.p.get_format_from_width(self.WIDTH),
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  output=True,
                                  frames_per_buffer=self.CHUNK)
        data = s.recv(1024)
        frames = []
        while data != '':
            self.Exit()
            try:
                self.stream2.write(data)
                data = s.recv(1024)
            except:
                self.flag = True
                break
            frames.append(data)
        self.flag = True
        self.Exit()
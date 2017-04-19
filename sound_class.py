import socket
import pyaudio
import wave
class OnlyAudio:
	def __init__(self,s):
		#record
		self.CHUNK = 1024
		self.FORMAT = pyaudio.paInt16
		self.CHANNELS = 1
		self.RATE = 44100
		self.RECORD_SECONDS = 40
		self.WIDTH = 2
		self.s = s
		self.p = pyaudio.PyAudio()

	def Send_Sound(self):
		self.stream = self.p.open(format=self.FORMAT,
		                channels=self.CHANNELS,
		                rate=self.RATE,
		                input=True,
		                frames_per_buffer=self.CHUNK)
		while True:
			print("*recording")
			frames = []
			for i in range(0, int(self.RATE/self.CHUNK*self.RECORD_SECONDS)):
				data  = self.stream.read(self.CHUNK)
				frames.append(data)
				self.s.sendall(data)
			print("*done recording")

	def Exit(self):
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()
		self.s.close()
		print("*closed")

	def Get_Sound(self):
		self.stream = self.p.open(format=self.p.get_format_from_width(self.WIDTH),
                channels=self.CHANNELS,
                rate=self.RATE,
                output=True,
                frames_per_buffer=self.CHUNK)
		data =self.s.recv(1024)
		i=1
		frames = []
		while data != '':
			self.stream.write(data)
			data = self.s.recv(1024)
			i=i+1
			print i
			frames.append(data)
		self.Exit()

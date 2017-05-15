import socket
import select
from twilio.rest import Client
import random
import pygeoip
import threading

class classclient:
    def __init__(self,ip):
        self.ip = ip
        self.rand = 0
        self.phonenum = 0
        GEOIP = pygeoip.GeoIP("GeoLiteCity.dat", pygeoip.MEMORY_CACHE)
        self.country = GEOIP.country_name_by_addr(self.ip)
class MyServer:
    def __init__(self):
        PORT1 = 5004
        IP = "0.0.0.0"
        self.s = socket.socket()
        self.s.bind((IP,PORT1))
        self.s.listen(10)
        self.clientlist = {}    #dictionar keys-socket values-class client
        self.donelist = {}
        mycheckthread = threading.Thread(target=self.send_con)
        mycheckthread.start()
        self.main_accept()

    def main_accept(self):
        while True:
            rlist, wlist, xlist = select.select([self.s] + self.clientlist.keys(), [], [])
            for current in rlist:
                if current is self.s:
                    print "new conn"
                    (newsock,address) = self.s.accept()    #create connection
                    self.clientlist[newsock] = classclient(address) #adds its values to dictionary

                else:
                    data = current.recv(1024)
                    if data.startswith("phone-"):
                        phone_num = data[6:]
                        print phone_num
                        self.clientlist[current].phonenum = phone_num   #gets the client that match the socket and turns its phone number to it
                        self.SMS_Verification(current)

                    elif data.startswith("num-"):
                        if self.check_verification(current,data[5:]):
                            self.donelist[current] = self.clientlist[current]
                    else:
                        current.close()
                        self.clientlist.pop(current)

    def SMS_Verification(self,current):
        accountSid = 'AC3f8357102c55bb262e49c7d5f09f3159'
        authToken = '341aa932b384a2bd54a2dd2acefae448'
        twilioClient = Client(accountSid, authToken)
        myTwilioNumber = "+17048938817"


        destCellPhone = self.clientlist[current].phonenum
        random_num = random.randint(1000,9999)
        messege = "You're verification number is : "+str(random_num)
        self.clientlist[current].rand = random_num
        myMessage = twilioClient.messages.create(body = messege, from_= myTwilioNumber, to = destCellPhone)
        print "sent"

    def check_verification(self,current,result):
        if self.clientlist[current].rand == result:
            return True
        else:
            return False

    def send_con(self):
        while True:
            for s1 in self.donelist.keys():
                for s2 in self.donelist.keys():
                    if s1 != s2 and self.donelist[s1].country == self.donelist[s2].country:
                        s1.send("client-"+self.donelist[s2].ip)
                        s2.send("server-"+self.donelist[s1].ip)
                        self.donelist.pop(s1)
                        self.donelist.pop(s2)


serv = MyServer()

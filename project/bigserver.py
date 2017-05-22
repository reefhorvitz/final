import socket
import select
#from twilio.rest import Client
import random
import pygeoip
import threading
import smtplib

class classclient:
    def __init__(self,ip):
        if ip == "127.0.0.1":
            ip == socket.gethostbyname(socket.gethostname())
        self.ip = ip
        self.rand = random.randint(1000,9999)
        print "his random is "+ str(self.rand)
        self.phonenum = 0
        print self.ip
        try:
            GEOIP = pygeoip.GeoIP("GeoLiteCity.dat", pygeoip.MEMORY_CACHE)
            self.country = GEOIP.country_name_by_addr(self.ip)
        except:
            self.country = "local"
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
                    self.clientlist[newsock] = classclient(address[0]) #adds its values to dictionary

                else:
                    try:
                        data = current.recv(1024)
                    except:
                        current.close()
                        self.clientlist.pop(current)
                    if data.startswith("phone-"):
                        phone_num = data[6:]
                        print phone_num
                        self.clientlist[current].phonenum = phone_num   #gets the client that match the socket and turns its phone number to it
                        self.send_email(current = current)

                    elif data.startswith("num-"):
                        print data
                        if self.check_verification(current,data[4:]):
                            self.donelist[current] = self.clientlist[current]
                    else:
                        current.close()
                        self.clientlist.pop(current)

    def check_verification(self,current,result):
        if str(self.clientlist[current].rand) == result:
            print result
            print "true"
            return True
        else:
            return False

    def send_con(self):
        while True:
            for s1 in self.donelist.keys():
                for s2 in self.donelist.keys():
                    if s1 != s2 and self.donelist[s1].country == self.donelist[s2].country:
                        print "creates Chat!"
                        s1.send("client-"+self.donelist[s2].ip)
                        s2.send("server-"+self.donelist[s1].ip)
                        self.donelist.pop(s1)
                        self.donelist.pop(s2)

    def send_email(self, user="reeffinal", pwd="reef12345", subject = "App confirmation DO NOT REPLY",current = ""):
        recipient = str(self.clientlist[current].phonenum)
        gmail_user = user
        gmail_pwd = pwd
        FROM = user
        TO = recipient if type(recipient) is list else [recipient]
        SUBJECT = subject
        TEXT = "Youre confiramation number - "+str(self.clientlist[current].rand)
        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, message)
            server.close()
            print 'successfully sent the mail'
        except:
            print "failed to send the mail"


serv = MyServer()

'''
    def SMS_Verification(self,current):
        accountSid = 'AC3f8357102c55bb262e49c7d5f09f3159'
        authToken = '341aa932b384a2bd54a2dd2acefae448'
        twilioClient = Client(accountSid, authToken)
        myTwilioNumber = "+17048938817"
        destCellPhone = self.clientlist[current].phonenum
        messege = "You're verification number is : "+str(self.clientlist[current].rand)
        myMessage = twilioClient.messages.create(body = messege, from_= myTwilioNumber, to = destCellPhone)
        print "sent"
        '''

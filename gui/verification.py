from twilio.rest import Client
def SMS_Verification(phone_num):
    accountSid = 'AC3f8357102c55bb262e49c7d5f09f3159'
    authToken = '341aa932b384a2bd54a2dd2acefae448'
    twilioClient = Client(accountSid, authToken)
    myTwilioNumber = "+17048938817"
    destCellPhone = phone_num
    myMessage = twilioClient.messages.create(body = "whatever", from_=myTwilioNumber, to=destCellPhone)

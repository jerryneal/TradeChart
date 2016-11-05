from twilio.rest import TwilioRestClient
from configParser import *
import smtplib
import logging

class SendMessage():

    def __init__(self):

        self.cf = ParseConfig()
        self.message = None

    def sendSMSMessage(self,message):

        try:
            server = smtplib.SMTP(self.cf.gmSetup,self.cf.gmPort)
            server.starttls()
            server.login(self.cf.chapUserName,self.cf.chapPassword)
            server.sendmail('API Test',self.cf.smsNumber, message)
            logging.debug('Message has been sent to Phone')
        except Exception as e:
            print e
            logging.debug('Message Not sent')

    def sendTwilioMessage(self,message):

        #Run client
        client = TwilioRestClient(self.cf.account_sid,self.cf.token)

        # try:
        #     message = client.sms.messages.create(to="+18023772744",from_="+15005550006",
        #                                  body='Were having a baby')
        #     # message = client.sms.messages.create()
        # except Exception as e:
        #     print e

        # print message, message.sid

    def sendEmailMessage(self,message):
        pass
#
# if __name__ == '__main__':




    # logging.basicConfig(format='%(asctime)s.%(msecs).03d - %(levelname)s - %(module)s.%(funcName)s: %(message)s \n</br>',datefmt='%d%b%Y %H:%M:%S',level=cf.loglevel)


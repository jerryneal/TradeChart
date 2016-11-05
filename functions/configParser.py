import ConfigParser
import os

class ParseConfig(object):
    '''
    Fetching and using config values
    '''

    def __init__(self):
        configfile = ""
        try:
            configfileName = 'configurationfile.ini'
            configfileName = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', configfileName))
            parser = ConfigParser.SafeConfigParser()
            parser.read(configfileName)
        except:
            raise Exception('Unable to read config file')

        self.parser = parser

        # Twillio messaging
        self.account_sid = parser.get('twilioMessaging','account_sid')
        self.token = parser.get('twilioMessaging','auth_token')

        # Database connection
        self.database = parser.get('databaseConnection','DATABASE')
        self.dbDebug = parser.get('databaseConnection','DEBUG')
        self.secretKey = parser.get('databaseConnection','SECRET_KEY')

        # In outbound Connections
        self.chapUserName = parser.get('inOutBoundConnections','chapUserName')
        self.chapPassword = parser.get('inOutBoundConnections','chapPassword')
        self.smsNumber = parser.get('inOutBoundConnections','smsNumber')
        self.mmsNumber = parser.get('inOutBoundConnections','mmsNumber')
        self.gmSetup = parser.get('inOutBoundConnections','gmSetup')
        self.gmPort = parser.get('inOutBoundConnections','gmPort')

        # Global Options
        self.loglevel = parser.get('globalOptions','loggingLevel')
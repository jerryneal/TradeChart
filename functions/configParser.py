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

        # Local host Database connection
        self.int_database_db = parser.get('localdatabaseConnection','MYSQL_DATABASE_DB')
        self.int_database_user = parser.get('localdatabaseConnection','MYSQL_DATABASE_USER')
        self.int_database_host = parser.get('localdatabaseConnection','MYSQL_DATABASE_HOST')
        self.int_database_pass = parser.get('localdatabaseConnection','MYSQL_DATABASE_PASSWORD')

        #External database connections
        self.ext_database_user = ('extDBConnection','MYSQL_DATABASE_USER')
        self.ext_database_pass = ('extDBConnection', 'MYSQL_DATABASE_PASSWORD')
        self.ext_database_db = ('extDBConnection','MYSQL_DATABASE_DB')
        self.ext_database_host = ('extDBConnection','MYSQL_DATABASE_HOST')

        # In outbound Connections
        self.chapUserName = parser.get('inOutBoundConnections','chapUserName')
        self.chapPassword = parser.get('inOutBoundConnections','chapPassword')
        self.smsNumber = parser.get('inOutBoundConnections','smsNumber')
        self.mmsNumber = parser.get('inOutBoundConnections','mmsNumber')
        self.gmSetup = parser.get('inOutBoundConnections','gmSetup')
        self.gmPort = parser.get('inOutBoundConnections','gmPort')

        # Global Options
        self.loglevel = parser.get('globalOptions','loggingLevel')
        self.secretKey = parser.get('globalOptions','secret_key')
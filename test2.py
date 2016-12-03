from flask import Flask
from flaskext.mysql import MySQL

server = 'malibu.mysql.pythonanywhere-services.com'
database = 'malibu$malibudb'
username = 'malibu'
password = 'testdbtestdb'


app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

if __name__ == '__main__':

    '''
        Attempt 1: Using mysql through flask
    '''
    # try:
    #     conn = mysql.connect()
    #     cursor =conn.cursor()
    #
    #     # Inserting data
    #     cursor.execute('insert into comments (comment,user,time) values(%s,%s,%s)', ('This is a comment', 'BradlyPBD', 'TBD'))
    #
    #     conn.commit()
    #
    #
    #     cursor.execute('SELECT id,comment,time,user from comments')
    #
    #     # cursor.execute("SELECT id from users where name = %s and password = %s", ())
    #     data = cursor.fetchall()
    #
    #     print "Success"
    # except Exception, e:
    #     print e
    # print data
    #
    # conn.close()


    '''
        Attempt 2: Using MySQL solo pickup
    '''
    try:
        import MySQLdb
        conn = MySQLdb.connect(
            host='malibu.mysql.pythonanywhere-services.com',
            user='<malibu>',
            passwd='<testdbtestdb>',
            db='<malibu>$<malibudb>',
            ssl={})
        print conn.ping()

        cursor = conn.cursor()
        cursor.execute("SELECT comment,user,time from comments order by id desc")
        data = cursor.fetchall()

        # cursor.execute("SELECT comment,user,time from comments order by id desc")

        print data
    except Exception, e:
        print e

    '''
        Atempt 3: Using Pyodbc
    '''

    # try:
    #     import pyodbc
    #     db = pyodbc.connect("driver={MySQL}, server=server, port=3306, database=database, uid=username, password=password;")
    #
    # except Exception, e:
    #     print ('Error Message:', e)

import os,logging
import datetime as dt
import MySQLdb
from flask import Flask, request, session, g, redirect, url_for, abort,render_template, flash
import functions
from flask.ext.mysql import MySQL
import subprocess

#Configuration Parser Information
cf = functions.configParser.ParseConfig()

# session.permanent = True

#the application object from the main Flask class
app = Flask(__name__)
mysql = MySQL()


#Configurations for hosted environment
app.config.update(dict(
    MYSQL_DATABASE_DB = cf.ext_database_db,
    MYSQL_DATABASE_USER = cf.ext_database_user,
    MYSQL_DATABASE_PASSWORD = cf.ext_database_pass,
    MYSQL_DATABASE_HOST = cf.ext_database_host,
    SECRET_KEY = cf.secretKey,
    DEBUG = cf.loglevel

))

app.config.from_envvar('TC_SETTINGS',silent=True)
    #do not complain if no config file exists

logging.basicConfig(format='%(asctime)s.%(msecs).03d - %(levelname)s - %(module)s.%(funcName)s: %(message)s \n</br>',datefmt='%d%b%Y %H:%M:%S',level=cf.loglevel)


def connect_db():
    pass



def get_db():
    # Opens a new connection to the MYSQL database
    # print cf.ext_database_port
    conn = MySQLdb.connect(host=cf.ext_database_host,user=cf.ext_database_user,passwd=cf.ext_database_pass,
                           db=cf.ext_database_db,port=int(cf.ext_database_port))
    # cmd = 'ssh -L 3333:malibu.mysql.pythonanywhere-services.com:3306 malibu@ssh.pythonanywhere.com'
    # conn =
    # conn = MySQLdb.connect(db='test', user='root', passwd='', host='localhost')
    cursor = conn.cursor()
    return conn


def init_db():
    # Creates the TC databse tables
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        try:
            #Creates tables within the tables
            with app.open_resource('tables.sql', mode='rb') as f:
                cursor.execute(f.read().replace("\r\n",""))
            # creates entries and user tables
        except:
            pass
        #Run the stored proc
        cursor.callproc('create_database_tables')
    db.commit()

@app.teardown_appcontext
def close_db(error):
    # db = get_db()
    # db.close()
    pass

@app.route('/')
def show_entries():
    # Render all entries of the TC database
    db = get_db()
    cursor = db.cursor(MySQLdb.cursors.DictCursor) # Error had something to with the Rowfactory
    cursor.execute("SELECT comment,user,time from comments order by id desc")
    comments = cursor.fetchall()
    logging.debug(comments)
    logging.debug("Entries should showed successfully")
    db.close()
    return render_template('show_entries.html', comments=comments)


@app.route('/register',methods=['GET','POST'])
def register():
    # Registers a new user in the TC database
    error = None
    if request.method == 'POST':
        db = get_db()
        if request.form['username'] == '' or request.form['password'] == '':
            error = 'Provide both a username and a password'
            # At this stage both fields have to be noneempty

        else:
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('insert into users (name, password) values (%s,%s)', [request.form['username'],request.form['password']])
            db.commit()
            logging.debug('Names registered into database')

        session['logged_in'] = True

        # Directly log in new user
        flash('You were successfully registered')
        app.config.update(dict(USERNAME = request.form['username']))
        return redirect(url_for('show_entries'))
    return render_template('register.html',error=error)

@app.route('/add', methods=['POST'])
def add_entry():
    # Adds entry to the TC database
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    now = dt.datetime.now()
    try:
        cursor = db.cursor()
        cursor.execute('insert into comments (comment, user, time) values (%s,%s,%s)',
                   [request.form['text'],app.config['USERNAME'],str(now)[:-7]])
    except Exception as e:
        logging.debug(e)
        flash('Item not added, please login and try again')
        session.pop('logged_in', None)
    db.commit()

    # Success Notifications
    flash('Your comment was successfully added.')
    logging.debug("Comment Successfully added")

    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET','POST'])
def login():
    'Logs in a user'
    error = None
    if request.method == 'POST':
        db = get_db()
        try:
            query = 'SELECT id from users where name = %s and password = %s'
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            id = cursor.execute(query, (request.form['username'],
                                    request.form['password'])).fetchone()[0]
            #fails if record with provided username and password is not found
            session['logged_in'] = True
            flash("You're logged in. YEY")
            logging.debug("Logging In was successful")
            app.config.update(dict(USERNAME=request.form['username']))
            return redirect(url_for('show_entries'))
        except:
            error = "User not found or wrong password"
            logging.debug("Logging in was not successful")
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    # Logs out the current user
    session.pop('logged_in', None)
    flash('You were logged out')
    logging.debug("Logging Out successful")
    return redirect(url_for('show_entries'))

#Adding a comment

if __name__ == '__main__':
    init_db() # comment out if data in currect
              # TC database if to be kept

    app.run()
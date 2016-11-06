import os,logging
import datetime as dt
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort,render_template, flash
import functions

#Configuration Parser Information
cf = functions.configParser.ParseConfig()

# session.permanent = True

#the application object from the main Flask class
app = Flask(__name__)

#override config from environment variable
app.config.update(dict(
    DATABASE = os.path.join(app.root_path, cf.database),
    DEBUG = cf.dbDebug,
    SECRET_KEY = cf.secretKey #secret key used here for real applications
))

app.config.from_envvar('TC_SETTINGS',silent=True)
    #do not complain if no config file exists

logging.basicConfig(format='%(asctime)s.%(msecs).03d - %(levelname)s - %(module)s.%(funcName)s: %(message)s \n</br>',datefmt='%d%b%Y %H:%M:%S',level=cf.loglevel)


def connect_db():
    #Connects to the database
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row  #TODO: What does this mean
    logging.debug('Database Connection Successful')
    return rv


def get_db():
    # Opens a new connection to the TC database
    if not hasattr(g, 'sqlite_db'):
        # open only if none exists yet
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    # Creates the TC databse tables
    with app.app_context():
        db = get_db()
        with app.open_resource('tables.sql', mode='rb') as f:
            db.cursor().executescript(f.read())
            # creates entries and user tables
    db.commit()

@app.teardown_appcontext
def close_db(error):
    # Closes the TC database at the end of the request
    # if hasattr(g, 'sqlite_db'):
    #     g.sqlite_db.close()
    pass

@app.route('/')
def show_entries():
    # Render all entries of the TC database
    db = get_db()
    query = "select comment,user,time from comments order by id desc"
    cursor = db.execute(query)
    comments = cursor.fetchall()
    logging.debug("Entries should showed successfully")
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
            db.execute('insert into users (name, password) values (?,?)', [request.form['username'],request.form['password']])
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
        db.execute('insert into comments (comment, user, time) values (?,?,?)',
                   [request.form['text'],app.config['USERNAME'],str(now)[:-7]])
    except Exception as e:
        logging.debug(e)
        flash('Item not added, please login and try again')
        session.pop('logged_in', None)
    # logging.DEBUG(app.config['USERNAME'])
    db.commit()

    # Send Message to Phone - To be included in Trigger
    # cm = functions.messaging.SendMessage()
    # cm.sendSMSMessage('FROM: %s'.join(app.config['USERNAME']))

    # cm.sendSMSMessage()

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
            query = 'select id from users where name = ? and password = ?'
            id = db.execute(query, (request.form['username'],
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
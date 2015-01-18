from flask import Flask, render_template, redirect, url_for, \
     request, session, flash, g
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy


#create application object
app = Flask(__name__)
app.config.from_object('config')

'''In a real situation the session key should be randomly generated, and imported.
The session key below is only for development purposes.'''
#app.secret_key = 'My-Session-Key'



#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://messages.db'

#create sqlalchemy object
db = SQLAlchemy(app)

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def home():
    #g.db = connect_db()
    #cur = g.db.execute()
    #posts = [dict()]
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials, please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html', error=error)   

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))
    
if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)

'''
def connect_db():
    pass
'''

from flask import Flask, render_template, redirect, url_for, \
     request, session, flash, g, jsonify, abort, make_response
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth

#create application object
app = Flask(__name__)
app.config.from_object('config')
auth = HTTPBasicAuth()

'''In a real situation the session key should be randomly generated, and imported.
The session key below is only for development purposes.'''
#app.secret_key = 'My-Session-Key'



#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://messages.db'

#create sqlalchemy object
db = SQLAlchemy(app)

'''---Begin code for web app---'''

# login required decorator for web app
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
        if request.form['username'] != 'levi' or request.form['password'] != 'python':
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

'''---End code for web app---'''

'''---Below is the code for the api---'''

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

#get password for api
@auth.get_password
def get_password(username):
    if username == 'levi':
        return 'python'
    return None

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/history/messages', methods=['GET'])
@auth.login_required
def get_all_messages():
    return jsonify({'tasks': tasks})

@app.route('/history/<int:task_id>', methods=['GET'])
@auth.login_required
def get_user_messages(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.route('/history/messages', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)

'''
def connect_db():
    pass
'''

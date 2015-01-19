from flask import Flask, render_template, redirect, url_for, \
     request, session, flash, g, jsonify, abort, make_response
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
#from models import Message
from datetime import datetime
from marshmallow import Schema, fields, ValidationError

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

### MODELS ###
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    contact = db.relationship('Contact',
        backref=db.backref('messages', lazy='dynamic'))

    def __init__(self, title, body, contact, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.contact = contact

    def __repr__(self):
        return '<Message %r>' % self.title


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Contact %r>' % self.name

### SCHEMAS ###

##### SCHEMAS #####

class ContactSchema(Schema):
    id = fields.Integer()
    name = fields.String()

    def must_not_be_blank(data):
        if not data:
            raise ValidationError('Data not provided.')
        
def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')

class MessageSchema(Schema):
    contact = fields.Nested(ContactSchema, validate=must_not_be_blank)
    title = fields.Str(required=True, validate=must_not_be_blank)

    class Meta:
        fields = ("id", "title", "body", 'pub_date', 'contact')

contact_schema = ContactSchema()
message_schema = MessageSchema()
messages_schema = MessageSchema(many=True, only=('id', 'title', 'body', 'contact'))


#get password for api
@auth.get_password
def get_password(username):
    if username == 'levi':
        return 'python'
    return None

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

'''
@app.route('/history/messages', methods=['GET'])
@auth.login_required
def get_all_messages():
    return jsonify({'tasks': tasks})
'''

#Retun all messages
@app.route('/history/messages/', methods=['GET'])
@auth.login_required
def get_all_messages():
    messages = Message.query.all()
    result = messages_schema.dump(messages)
    return jsonify({"messages": result.data})

#Return all messages for a certain contact
@app.route('/history/<string:name>', methods=['GET'])
@auth.login_required
def get_user_messages(name):
    try:
        #contact = Contact.query.get(name)
        contact = Contact.query.filter_by(name=name).first()
    except IntegrityError:
        return jsonify({"message": "Contact could not be found."}), 400
    contact_result = contact_schema.dump(contact)
    messages_result = messages_schema.dump(contact.messages.all())
    return jsonify({'contact': contact_result.data, 'messages': messages_result.data})


@app.route('/history/<string:name>', methods=['POST'])
@auth.login_required
def new_message(name):
    if not request.get_json():
        return jsonify({'message': 'No input data provided'}), 400    
 
    contact_name = name       
    title_input = request.get_json().get('Title')
    message_input = request.get_json().get('Message')
    input_data = dict(contact=contact_name, title=title_input, message=message_input) 
    contact = Contact.query.filter_by(name=name).first()
    if contact is None:
        # Create a new author
        contact = Contact(name)
        db.session.add(contact)
    
    # Create new quote
    message = Message(title_input, message_input, contact)
    db.session.add(message)
    db.session.commit()
    result = message_schema.dump(Message.query.get(message.id))
    return jsonify({"message": "Created new message!",
                    "message": result.data})
   

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)

'''
def connect_db():
    pass
'''

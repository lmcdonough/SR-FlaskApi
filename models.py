from app import db

class Messages(db.Model):

    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    message = db.Column(db.Text, nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'))
    timestamp = db.Column(db.DateTime)
'''    
    def __init__(self, title, message):
        self.title = title
        self.message = message
'''
        def __repr__(self):
            return 'title {}'.format(self.title)


class Contacts(db.Model):

    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    contact_name = db.Column(db.String(120))
    messages = db.relationship('Messages', backref='contact', lazy='dynamic')

    def __repr__(self):
        return 'contact {}'.format(self.contact_name)

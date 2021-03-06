from application import db
from application import login_manager
from flask_login import UserMixin
from datetime import datetime

#create a table Posts
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.String(500), nullable=False, unique=True)
    
    #printable version also known as self representation
    def __repr__(self):
        return ''.join([
            'User ID: ', self.user_id, '\r\n',
            'Title: ', self.title, '\r\n', self.content
            ])


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))        

#creates a table Users
class Users(db.Model,UserMixin): #we need to subclass UserMixin or we get the error  'Users' object has no attribute 'is_active'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False) #add the first name to the user table
    last_name = db.Column(db.String(30), nullable=False) #add the loast name to the user table
    email = db.Column(db.String(500), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    posts = db.relationship('Posts', backref='author', lazy=True)

    #printable version also known as self representation
    def __repr__(self):
        return ''.join([
            'User ID: ', str(self.id), '\r\n',
            'Email: ', self.email, '\r\n',
            'Name: ', self.first_name, ' ', self.last_name
        ])

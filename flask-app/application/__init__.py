# import Flask class from the flask module
from flask import Flask

from flask_sqlalchemy import SQLAlchemy 

#import Bcrypt to hash the user password
from flask_bcrypt import Bcrypt

#import Login Manager to make possible user login
from flask_login import LoginManager

import os


# create a new instance of Flask and store it in app 
app = Flask(__name__) 

app.config['SQLALCHEMY_DATABASE_URI'] = str(os.getenv('DATABASE_URI'))

app.config['SECRET_KEY'] = str(os.getenv('MY_SECRET_KEY'))

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login' #redirect not logged user to the login page

# import the ./application/routes.py file  --- this must always be at the enf of this __init__.py file
from application import routes



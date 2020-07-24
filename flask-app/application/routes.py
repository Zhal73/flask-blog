# import render_template function from the flask module
from flask import render_template
# import the app object from the ./application/__init__.py
from application import app

from application.models import Posts

# define routes for / & /home, this function will be called when these are accessed
@app.route('/')
@app.route('/home')
def home():
    postData = Posts.query.all()
    return render_template('home.html', title='Home', posts=postData)

@app.route('/about')
def about():
    return render_template('about.html',title='About')

@app.route('/login')
def login():
    return render_template('login.html',title='Login')

@app.route('/register')
def register():
    return render_template('register.html',title='Register')

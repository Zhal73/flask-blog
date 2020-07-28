from application import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from application.models import Posts, Users
from application.forms import PostForm, RegistrationForm, LoginForm, UpdateAccountForm
from flask import render_template, redirect, url_for, request

@app.route('/')
@app.route('/home')
@login_required
def home():
    postData = Posts.query.all()
    return render_template('home.html',name=current_user.first_name, title='Home', posts=postData)

@app.route('/about')
@login_required
def about():
    return render_template('about.html',title='About')

@app.route('/post', methods=['GET', 'POST'])
@login_required #the user can access the post page only if is logged in
def post():
    form = PostForm()
    if form.validate_on_submit():
        postData = Posts(
            title = form.title.data,
            content = form.content.data,
            author = current_user
        )

        db.session.add(postData)
        db.session.commit()

        return redirect(url_for('home'))

    else:
        print(form.errors)

    return render_template('post.html', title='Post', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data)

        user = Users(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=hash_pw
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('post'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

#once the user is logged out it is redirected to the login page.
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

#define the rout for the page to chenge user details
@app.route("/account", methods=['GET', 'POST'])
def account():
    form = UpdateAccountForm() #import the form
    #if the form submitted fine
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('home'))
    #else return the existing User's informations
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

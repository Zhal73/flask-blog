from application import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from application.models import Posts, Users
from application.forms import PostForm, RegistrationForm, LoginForm, UpdateAccountForm
from flask import render_template, redirect, url_for, request

@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        postData = Posts.query.all()
        return render_template('home.html',name=current_user.first_name, title='Home', posts=postData)
    else:
        return render_template('home.html', title='Home')

@app.route('/about')
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
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#defines the route for the page to chenge user details
@app.route("/account", methods=['GET', 'POST'])
@login_required
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

#delete an user from the database
@app.route("/account/delete", methods=["GET", "POST"])
@login_required
def account_delete():
    user = current_user.id  #gets the id of the user currently logged in
    account = Users.query.filter_by(id=user).first() #retrieves the corresponding record from the database
    posts_to_delete = Posts.query.filter_by(user_id = user).all() #retireves all the posts from the user
    
    #deletes each post
    for post in posts_to_delete:
        db.session.delete(post)

    logout_user() # logs the user out
    db.session.delete(account)
    db.session.commit()
    return redirect(url_for('register')) #redirects. No reder template returned



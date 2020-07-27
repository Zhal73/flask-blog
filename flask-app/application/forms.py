#class FlaskForm to create a Form
from flask_wtf import FlaskForm
#WTForm field type
from wtforms import StringField, SubmitField, PasswordField
#WTForm validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
#Import the User class we defined in models.py
from application.models import Users

#Form to insert a post on the db
class PostForm(FlaskForm):
    first_name = StringField('First Name',
        validators = [
            DataRequired(),
            Length(min=2, max=30)
        ]
    )
    last_name = StringField('Last Name',
        validators = [
            DataRequired(),
            Length(min=2, max=30)
        ]
    )
    title = StringField('Title',
        validators = [
            DataRequired(),
            Length(min=2, max=100)
        ]
    )
    content = StringField('Content',
        validators = [
            DataRequired(),
            Length(min=2, max=1000)
        ]
    )
    submit = SubmitField('Post!')

#Form to insert a new user in the db --- Registration form
class RegistrationForm(FlaskForm):
    email = StringField('Email',
        validators = [
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField('Password',
        validators = [
            DataRequired()
        ]
    )
    confirm_password = PasswordField('Confirm Password',
        validators = [
            DataRequired(),
            EqualTo('password')
        ]
    )
    submit = SubmitField('Sign Up')

    #this function performs a validation on the email field
    #makes sure that the email is not already used 
    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Email already in use')

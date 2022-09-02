from email import message
from typing_extensions import Required
from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256

from models import User

def invalid_credentials(form, field):
    """Username and password checker"""

    username_entered = form.username.data
    password_entered = field.data

    # check username is valid
    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError("Username or Password is incorrect")
    elif  not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("username or passwaord is incorrect")


class RegistrationForm(FlaskForm):
    """ Registration form """

    username = StringField('username_label',validators=[InputRequired(message="Username Required"),
    Length(min=4,max=25, message="Usename must be between 4 to 25 characters")])
    password = PasswordField('password_label',validators=[InputRequired(message="Password Required"),
    Length(min=4,max=25, message="Password must be between 4 to 25 characters")])
    confirm_pswd = PasswordField('confirm_pswd_label',validators=[InputRequired(message="Password Required"),EqualTo('password',message="Password must match")])
    submit_button = SubmitField('Create')

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username Already exist , Select different Username.")


class LoginForm(FlaskForm):
    """Login Form"""

    username = StringField('username_label',
        validators=[InputRequired(message="Username required")])
    password = PasswordField('password_label',
        validators=[InputRequired(message="password required"),
        invalid_credentials])
    submit_button = SubmitField('Log In')



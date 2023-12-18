from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, EmailField

from ..models import User


class UserSignupValidation(FlaskForm):
    email = EmailField("Email", validators=[
        validators.DataRequired(),
    ])
    username = StringField("Username", validators=[
        validators.DataRequired(),
        validators.Length(min=6, max=256)
    ])
    first_name = StringField("First name", validators=[
        validators.DataRequired(),
        validators.Length(min=4, max=256)
    ])
    last_name = StringField("Last name", validators=[
        validators.DataRequired(),
        validators.Length(min=4, max=256)
    ])
    photo_url = StringField('Photo')
    contact_number = StringField("Contact Number", validators=[
        validators.DataRequired(),
        validators.Length(min=10, max=11),
    ])
    password = PasswordField('New Password', validators=[
        validators.Length(min=6, max=25),
        validators.EqualTo('confirm_password', message='Passwords must match'),
          validators.Regexp(regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,25}$',
                          message='Password must contain at least one lowercase letter, one uppercase letter, one number, and one special character')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        validators.Length(min=6, max=25),
        validators.EqualTo('password', message='Passwords must match')
    ])

    def validate_username(self, field):
        if User.check_if_username_exists(field.data):
            raise validators.ValidationError(
                'Username already existed')

    def validate_email(self, field):
        if User.check_if_email_exists(field.data):
            raise validators.ValidationError(
                'Email address already existed')

    def validate_contact_number(self, field):
        if User.check_if_contact_number_exists(field.data):
            raise validators.ValidationError(
                'Contact Number already existed')


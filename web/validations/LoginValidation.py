from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class LoginValidation(FlaskForm):
  username = StringField("Username", validators=[validators.DataRequired()])
  password = PasswordField("Password", validators=[validators.DataRequired()])
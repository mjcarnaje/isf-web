from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import PasswordField, StringField, validators

from ..models import User


class AdminLoginValidation(FlaskForm):
  username = StringField("Username", validators=[validators.DataRequired()])
  password = PasswordField("Password", validators=[validators.DataRequired()])

  def validate_username(self, field):      
      if not User.check_if_username_exists(field.data):
          raise validators.ValidationError(
              'Username does not exist')

  def validate_password(self, field):
      admin = User.find_by_username(username=self.username.data)

      if admin and not check_password_hash(admin.password, field.data):
          raise validators.ValidationError(
              'Password is incorrect')

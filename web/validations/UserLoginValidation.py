from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import PasswordField, StringField, validators

from ..models import User, UserRole


class UserLoginValidation(FlaskForm):
  username = StringField("Username", validators=[validators.DataRequired()])
  password = PasswordField("Password", validators=[validators.DataRequired()])

  def validate_username(self, field):
    if not User.check_if_username_exists(field.data):
        raise validators.ValidationError(
            'Username does not exist'
        )
      
    if UserRole.check_user_role_by_username(field.data, "admin"):
        raise validators.ValidationError(
            'You should login as admin.'
        )

  def validate_email(self, field):
    if not User.check_if_username_exists(field.data):
        raise validators.ValidationError(
            'Email does not exist')
    if UserRole.check_user_role_by_email(field.data, "admin"):
        raise validators.ValidationError(
            'You should login as admin'
        )

      

  def validate_password(self, field):
    user = User.find_by_username(username=self.username.data)

    if user and not check_password_hash(user.password, field.data):
        raise validators.ValidationError(
            'Password is incorrect')
    
    

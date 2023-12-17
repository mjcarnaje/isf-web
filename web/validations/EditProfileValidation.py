from flask_wtf import FlaskForm
from wtforms import StringField, validators, EmailField, HiddenField

from ..models import User


class EditProfileValidation(FlaskForm):
    id = HiddenField('Id')
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
    def validate_username(self, field):
        if User.check_if_username_exists(field.data, self.id.data):
            raise validators.ValidationError(
                'Username already existed')

    def validate_contact_number(self, field):
        if User.check_if_contact_number_exists(field.data, self.id.data):
            raise validators.ValidationError(
                'Contact Number already existed')


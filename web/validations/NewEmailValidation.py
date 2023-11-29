from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, validators, EmailField

from ..models import User


class NewEmailValidation(FlaskForm):
    id = HiddenField()
    old_email = HiddenField()
    email = EmailField("New Email", validators=[
        validators.DataRequired(),
    ])

    def validate_email(form, field):
        if field.data == form.old_email.data:
            raise validators.ValidationError(
                'Should not match to your old email.')

        if User.check_if_email_exists(field.data, form.id.data):
            raise validators.ValidationError(
                'Email address already existed')

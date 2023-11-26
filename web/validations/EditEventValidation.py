from flask_wtf import FlaskForm
from wtforms import StringField, validators, DateField, BooleanField, TextAreaField, HiddenField

from ..models import Event
from datetime import date


class EditEventValidation(FlaskForm):
    id = HiddenField("Id")
    name = StringField("Name", validators=[validators.DataRequired()])
    description = TextAreaField("Description", validators=[
        validators.DataRequired(),
        validators.Length(min=24)
    ], render_kw={"placeholder": "Description"})
    cover_photo_url = StringField("Cover Photo", validators=[
        validators.DataRequired()
    ])
    start_date = DateField("Start Date", format='%Y-%m-%d', validators=[
        validators.DataRequired(),
    ])
    end_date = DateField("End Date", format='%Y-%m-%d', validators=[
        validators.DataRequired(),
    ])
    location = StringField("Location", validators=[
        validators.DataRequired()
    ])
    show_in_landing = BooleanField("Show in Landing")
    
    def validate_start_date(form, field):
        if field.data <= date.today():
            raise validators.ValidationError("Start date must be set to a future date.")

    
    def validate_end_date(form, field):
        if field.data < form.start_date.data:
            raise validators.ValidationError("End date must not be earlier than start date.")
    
    def validate_name(form, field):
        if Event.check_if_event_exists(field.data, form.id.data):
            raise validators.ValidationError("Event name already exists.")
from flask_wtf import FlaskForm
from wtforms import StringField, validators, DateField, BooleanField, SelectField, TextAreaField, FieldList

from ..models import Event
from datetime import date


class AddEventValidation(FlaskForm):
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
    who_can_see_it = SelectField('Who can see it?', choices=[
                         ("Public", "Public"), 
                         ("Verified User", "Verified User"),
                         ], validators=[validators.DataRequired()])
    
    who_can_join = SelectField('Who can join?', choices=[("Anyone", "Anyone"), ("Invite Only", "Invite Only (Invite All Volunteers)")], validators=[validators.DataRequired()])

    pictures = FieldList(StringField(), label="Photos")    
    
    def validate_end_date(form, field):
        if field.data < form.start_date.data:
            raise validators.ValidationError("End date must not be earlier than start date.")
    
    def validate_name(form, field):
        if Event.check_if_event_exists(field.data):
            raise validators.ValidationError("Event name already exists.")
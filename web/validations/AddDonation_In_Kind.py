from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, validators, RadioField

class AddDonation_In_Kind(FlaskForm):
    evidence_pictures = StringField("Evidence Pictures", validators=[validators.DataRequired()])                                
    description = TextAreaField("Description", validators=[validators.DataRequired()], render_kw={
        'placeholder': "In-Kind Donation Description"})
    pick_up_location = StringField("Pick-Up Location", validators=[validators.DataRequired()], render_kw={
        'placeholder': "Enter Location"})
    delivery_type = RadioField("Delivery Type", choices=[
        ("pickup", "Pick Up"), ("deliver", "Deliver")
    ])
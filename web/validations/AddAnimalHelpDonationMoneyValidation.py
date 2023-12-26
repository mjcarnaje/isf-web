from flask_wtf import FlaskForm
from wtforms import validators, IntegerField, widgets, FieldList, StringField

class AddAnimalHelpDonationMoneyValidation(FlaskForm):
    amount = IntegerField("Amount", widget=widgets.NumberInput())
    pictures = FieldList(StringField(), label="Pictures", validators=[validators.DataRequired()])
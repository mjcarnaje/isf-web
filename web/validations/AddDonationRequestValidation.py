from flask_wtf import FlaskForm
from wtforms import HiddenField, TextAreaField, validators, IntegerField, widgets, FieldList, StringField

class AddDonationRequestValidation(FlaskForm):
    animal_id = HiddenField("Animal Id")
    description = TextAreaField("Description", validators=[
        validators.DataRequired(),
        validators.Length(min=10)
    ], render_kw={"placeholder": "Description"})
    amount = IntegerField("Amount", widget=widgets.NumberInput(), validators=[
        validators.DataRequired(),
    ])
    item_list = TextAreaField("Item List (Separate by comma ,)", validators=[validators.DataRequired()], render_kw={
        'placeholder': "List all the items (separate by comma ,)",
    })
    pictures = FieldList(StringField(), label="Current Status", validators=[validators.DataRequired()])
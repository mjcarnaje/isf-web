from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, validators, SelectField, FieldList

class AddDonation_In_Kind(FlaskForm):
    item_list = TextAreaField("Item List (Separate by comma ,)", validators=[validators.DataRequired()], render_kw={
        'placeholder': "List all the items (separate by comma ,)",
    })
    remarks = TextAreaField("Remarks", validators=[validators.DataRequired()], render_kw={
        'placeholder': "Remarks",
    })
    pick_up_location = StringField("Pick-Up Location", render_kw={
        'placeholder': "Enter Location"
    })
    delivery_type = SelectField("Delivery Type", choices=[
        ("Pick-up", "Pick-up"), ("Deliver", "Deliver")
    ])
    pictures = FieldList(StringField(), label="Pictures", validators=[validators.DataRequired()])
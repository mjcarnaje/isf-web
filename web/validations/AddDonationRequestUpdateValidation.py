from flask_wtf import FlaskForm
from wtforms import HiddenField, TextAreaField, validators, IntegerField, widgets, FieldList, StringField

class AddDonationRequestUpdateValidation(FlaskForm):
    animal_id = HiddenField("Donation Request Id")
    update_text = TextAreaField("Description", validators=[
        validators.DataRequired(),
        validators.Length(min=10)
    ], render_kw={"placeholder": "Description"})
    pictures = FieldList(StringField(), label="Pictures", validators=[validators.DataRequired()])
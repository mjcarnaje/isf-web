from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators, FieldList, StringField

class AddDonationRequestDonationInKindValidation(FlaskForm):
    item_list = TextAreaField("Item List (Separate by comma ,)", render_kw={
        'placeholder': "List all the items (separate by comma ,)",
    })
    pictures = FieldList(StringField(), label="Pictures", validators=[validators.DataRequired()])
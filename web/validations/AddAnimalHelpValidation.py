from flask_wtf import FlaskForm
from wtforms import HiddenField, TextAreaField, validators, IntegerField, widgets, FieldList, StringField

class AddAnimalHelpValidation(FlaskForm):
    animal_id = HiddenField("Animal Id")
    thumbnail_url = StringField("Thumbnail", validators=[
        validators.DataRequired()
    ])
    description = TextAreaField("Description", validators=[
        validators.DataRequired(),
        validators.Length(min=10)
    ], render_kw={"placeholder": "Description"})
    amount = IntegerField("Amount", widget=widgets.NumberInput(), validators=[
        validators.DataRequired(),
    ])
    item_list = TextAreaField("Wish list (Optional)", render_kw={
        'placeholder': "Wish list (separate by comma ,)",
    })
from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators, IntegerField, widgets, StringField

class EditAnimalHelpValidation(FlaskForm):
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
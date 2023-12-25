from flask_wtf import FlaskForm
from wtforms import TextAreaField, FieldList, StringField

class AddEventPostValidation(FlaskForm):
    post_text = TextAreaField("Caption", render_kw={
            'placeholder': "Type Caption..",
        })
    pictures = FieldList(StringField(), label="Pictures")
from flask_wtf import FlaskForm
from wtforms import HiddenField, TextAreaField, validators, FieldList, StringField

class AddAnimalHelpPostValidation(FlaskForm):
    animal_help_id = HiddenField("Animal Help Id")
    post_text = TextAreaField("Description", validators=[
        validators.DataRequired(),
    ], render_kw={"placeholder": "Description"})
    pictures = FieldList(StringField(), label="Pictures")
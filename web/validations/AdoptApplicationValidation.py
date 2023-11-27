from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators


class AdoptApplicationValidation(FlaskForm):
  reason_to_adopt = TextAreaField("Reason", validators=[
    validators.DataRequired(),
   
  ], render_kw={
      'description': 'Reasons to adopt.'
    })
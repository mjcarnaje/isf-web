from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, validators

class AddDonation_In_Kind(FlaskForm):
  evidence_pictures = StringField("Evidence Pictures", validators=[validators.DataRequired()])
  description = TextAreaField("Description", validators=[validators.DataRequired()])

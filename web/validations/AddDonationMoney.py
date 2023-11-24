from flask_wtf import FlaskForm
from wtforms import StringField, validators

class AddDonationMoney(FlaskForm):
  description = StringField("Description", validators=[validators.DataRequired()])
  evidence_pictures = StringField("Evidence Pictures", validators=[validators.DataRequired()])
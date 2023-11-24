from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, validators

class AddDonationMoney(FlaskForm):
  description = TextAreaField("Description", validators=[validators.DataRequired()], render_kw={
      'label': "Receipt Description",
     
  })
  evidence_pictures = StringField("Evidence Pictures", validators=[validators.DataRequired()])
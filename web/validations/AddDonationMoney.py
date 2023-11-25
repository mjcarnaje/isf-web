from flask_wtf import FlaskForm
from wtforms import TextAreaField, FieldList, validators, StringField, IntegerField, widgets

class AddDonationMoney(FlaskForm):
  amount = IntegerField("Amount", widget=widgets.NumberInput(), validators=[
    validators.DataRequired(),
  ])
  remarks = TextAreaField("Remarks", validators=[validators.DataRequired()], render_kw={
      'placeholder': "Remarks",
  })
  pictures = FieldList(StringField(), label="Screenshots / Receipts", validators=[validators.DataRequired()])
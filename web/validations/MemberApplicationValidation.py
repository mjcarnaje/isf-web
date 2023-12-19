from flask_wtf import FlaskForm
from wtforms import HiddenField, validators, TextAreaField



class MemberApplicationValidation(FlaskForm):
    id = HiddenField()
    join_reason = TextAreaField("Reason for Joining", validators=[
        validators.DataRequired(),
        validators.Length(min=20)
    ], render_kw={"placeholder": "Share your reasons for wanting to join."})

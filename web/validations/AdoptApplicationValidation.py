from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators, SelectField, DateField
from datetime import datetime, timedelta

def get_select_time(start, end, interval):
    start_time = datetime.strptime(start, '%I:%M %p')
    end_time = datetime.strptime(end, '%I:%M %p')
    
    result = []

    current_time = start_time
    while current_time <= end_time:
        formatted_time = current_time.strftime('%I:%M %p')
        result.append((formatted_time, formatted_time))
        current_time += timedelta(minutes=interval)

    return result


class AdoptApplicationValidation(FlaskForm):
  interview_type_preference = SelectField("Interview Type Preference", choices=[('Phone', 'Phone'), ('Zoom', 'Zoom'), ('Google Meet', 'Google Meet')], validate_choice=False)
  interview_preferred_date = DateField('Interview Preffered Date', validators=[
    validators.DataRequired(),
  ])
  interview_preferred_time = SelectField("Interview Preffered Time", choices=get_select_time('8:00 AM', '9:00 PM', 30), validate_choice=False)
  reason_to_adopt = TextAreaField("Why do you want to adopt?", validators=[
    validators.DataRequired(),
  ], render_kw={
      'description': 'Reasons to adopt.'
    })
import datetime

from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateField, SelectField, StringField,
                     TextAreaField, validators)


def get_years(year_from: int):
    year_to = datetime.datetime.now().year
    return [(year, year) for year in range(year_to, year_from - 1, -1)]

def get_months():
    return [
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December')
    ]


class AnimalValidation(FlaskForm):
    name = StringField("Name", validators=[validators.DataRequired()])
    type = SelectField('Type', choices=[
                         ("dog", "Dog"), ("cat", "Cat")], validators=[validators.DataRequired()])
    estimated_birth_month = SelectField("Estimated Birth Month", choices=get_months(), validate_choice=False)
    estimated_birth_year = SelectField("Estimated Birth Year", choices=get_years(2003),validators=[validators.DataRequired()])
    photo_url = StringField("Photo", validators=[validators.DataRequired()])
    gender = SelectField('Gender', choices=[
                         ("male", "Male"), ("female", "Female")])   
    is_adopted = BooleanField("Adopted")
    is_dead = BooleanField("Dead")
    is_dewormed = BooleanField("Dewormed")
    is_neutered = BooleanField("Neutered")
    in_shelter = BooleanField("In Shelter")
    is_rescued = BooleanField("Rescued")
    description = TextAreaField("Description", validators=[validators.DataRequired()], render_kw={"placeholder": "Description"})
    appearance = TextAreaField("Appearance", validators=[validators.DataRequired()])
import datetime

from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateField, HiddenField, SelectField,
                     StringField, TextAreaField, validators)

from ..models import Animal


def get_years(year_from: int):
    year_to = datetime.datetime.now().year
    return [(year, year) for year in range(year_to, year_from - 1, -1)]

def get_months():
    return [
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December')
    ]


class EditAnimalValidation(FlaskForm):
    id = HiddenField("Id")
    name = StringField("Name", validators=[validators.DataRequired()])
    type = SelectField('Type', choices=[
                         ("Dog", "Dog"), ("Cat", "Cat")], validators=[validators.DataRequired()])
    estimated_birth_month = SelectField("Estimated Birth Month", choices=get_months(), validate_choice=False)
    estimated_birth_year = SelectField("Estimated Birth Year", choices=get_years(2003),validators=[validators.DataRequired()])
    photo_url = StringField("Photo", validators=[validators.DataRequired()])
    gender = SelectField('Gender', choices=[
                         ("Male", "Male"), ("Female", "Female")])   
    is_dead = BooleanField("Deceased")
    is_dewormed = BooleanField("Dewormed")
    is_neutered = BooleanField("Neutered")
    in_shelter = BooleanField("In Shelter")
    is_rescued = BooleanField("Rescued")
    description = TextAreaField("Description", validators=[validators.DataRequired()], render_kw={"placeholder": "Description"})
    appearance = TextAreaField("Appearance", validators=[validators.DataRequired()])

    def validate_name(form, field):
        if Animal.check_if_animal_exists(field.data, form.id.data):
            raise validators.ValidationError("Animal name already in use. If this is intentional, please add a '#' after the name.")
from flask import Blueprint, redirect, render_template, request, url_for

from ...models import Animal
from ...utils import admin_required
from ...validations import AnimalValidation
from flask_login import current_user

admin_rescue_bp = Blueprint("rescue", __name__, url_prefix='/rescue')

@admin_rescue_bp.route('/', methods=['GET'])
@admin_required
def animals():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query', '', type=str)

    animals_query = Animal.find_all(
        page_number=page,
        page_size=12,
        query=query,
    )

    animals = animals_query.get("data")
    has_previous_page = animals_query.get("has_previous_page")
    has_next_page = animals_query.get("has_next_page")
    total_count = animals_query.get("total_count")

    return render_template('admin/animals/list.html', animals=animals, has_previous_page=has_previous_page, has_next_page=has_next_page, total_count=total_count)

@admin_rescue_bp.route('/add-animal', methods=['GET', 'POST'])
@admin_required
def add_animal():
  form = AnimalValidation()

  if form.validate_on_submit():
    name = form.name.data
    type = form.type.data
    estimated_birth_month = form.estimated_birth_month.data
    estimated_birth_year = form.estimated_birth_year.data
    photo_url = form.photo_url.data
    gender = form.gender.data
    is_adopted = form.is_adopted.data
    is_dead = form.is_dead.data
    is_dewormed = form.is_dewormed.data
    is_neutered = form.is_neutered.data
    in_shelter = form.in_shelter.data
    is_rescued = form.is_rescued.data
    description = form.description.data
    appearance = form.appearance.data
    author_id = current_user.id

    animal_id = Animal.insert(
      name=name,
      type=type,
      estimated_birth_month=estimated_birth_month,
      estimated_birth_year=estimated_birth_year,
      photo_url=photo_url,
      gender=gender,
      is_adopted=is_adopted,
      is_dead=is_dead,
      is_dewormed=is_dewormed,
      is_neutered=is_neutered,
      in_shelter=in_shelter,
      is_rescued=is_rescued,
      description=description,
      appearance=appearance,
      author_id=author_id
    )

    if animal_id:
       return redirect(url_for('admin.rescue.index'))


  return render_template('admin/animals/add_animal.html', form=form)


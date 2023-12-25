from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)
from flask_login import current_user

from ...config import Config
from ...models import Animal
from ...utils import admin_required, get_active_filter_count
from ...validations import AddAnimalValidation, EditAnimalValidation
from ...utils import pagination

animal_bp = Blueprint("animal", __name__, url_prefix='/animals')

@animal_bp.route('', methods=['GET'])
@admin_required
def animals():
    page = request.args.get('page', 1, type=int)
    view_type = session.get('view_type')

    filters = {
        'query': request.args.get('query', '', type=str),
        'for_adoption': request.args.get('for_adoption') == 'on',
        'is_rescued': request.args.get('is_rescued') == 'on',
        'is_adopted': request.args.get('is_adopted') == 'on',
        'is_dead': request.args.get('is_dead') == 'on',
        'is_dewormed': request.args.get('is_dewormed') == 'on',
        'is_neutered': request.args.get('is_neutered') == 'on',
        'in_shelter': request.args.get('in_shelter') == 'on',
        'gender': request.args.get('gender'),
        'type': request.args.get('type')
    }

    animals_query = Animal.find_all(
        page_number=page,
        page_size=Config.DEFAULT_PAGE_SIZE,
        filters=filters
    )

    animals = animals_query.get("data")
    total_count = animals_query.get("total_count")
    offset = animals_query.get("offset")

    return render_template('admin/animal/animals.html', 
        animals=animals,
        filters=filters,
        active_filters=get_active_filter_count(filters),
        view_type=view_type,
        pagination = pagination(
            page_number=page,
            offset=offset,
            page_size=Config.DEFAULT_PAGE_SIZE,
            total_count=total_count,
            base_url="admin.animal.animals"
        ),
    )

@animal_bp.route('/<int:id>', methods=['GET'])
@admin_required
def view_animal(id):
  animal = Animal.find_by_id(id)
  adopter = Animal.get_adopter(id)
  return render_template('/admin/animal/animal.html', animal=animal, adopter=adopter)  
  
@animal_bp.route('/add-animal', methods=['GET', 'POST'])
@admin_required
def add_animal():
  form = AddAnimalValidation()

  if form.validate_on_submit():
    name = form.name.data
    type = form.type.data
    estimated_birth_month = form.estimated_birth_month.data
    estimated_birth_year = form.estimated_birth_year.data
    photo_url = form.photo_url.data
    gender = form.gender.data
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
       return redirect(url_for('admin.animal.animals'))


  return render_template('admin/animal/add.html', form=form)

@animal_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_animal(id):
    animal = Animal.find_by_id(id)
    form = EditAnimalValidation()

    if form.validate_on_submit():
        animal.name = form.name.data
        animal.type = form.type.data
        animal.estimated_birth_month = form.estimated_birth_month.data
        animal.estimated_birth_year = form.estimated_birth_year.data
        animal.photo_url = form.photo_url.data
        animal.gender = form.gender.data
        animal.is_dead = form.is_dead.data
        animal.is_dewormed = form.is_dewormed.data
        animal.is_neutered = form.is_neutered.data
        animal.in_shelter = form.in_shelter.data
        animal.is_rescued = form.is_rescued.data
        animal.description = form.description.data
        animal.appearance = form.appearance.data

        Animal.edit(animal)
        
        return redirect(url_for("admin.animal.animals"))
    
    if not form.is_submitted():
        form.id.data = animal.id
        form.name.data = animal.name
        form.type.data = animal.type
        form.photo_url.data = animal.photo_url
        form.estimated_birth_month.data = animal.estimated_birth_month
        form.estimated_birth_year.data = animal.estimated_birth_year
        form.gender.data = animal.gender
        form.description.data = animal.description
        form.appearance.data = animal.appearance
        form.is_dead.data = animal.is_dead == 1
        form.is_dewormed.data = animal.is_dewormed == 1
        form.is_neutered.data = animal.is_neutered == 1
        form.in_shelter.data = animal.in_shelter == 1
        form.is_rescued.data = animal.is_rescued == 1
            
    return render_template('admin/animal/edit.html', form=form, animal=animal)

@animal_bp.route('/<id>/delete', methods=['DELETE'])
@admin_required
def delete_animal(id):
    animal = Animal.find_by_id(id)

    if not animal:
        return {"error": "Animal not found"}, 404

    Animal.delete(id)
    
    return "success"
    
@animal_bp.route('/<id>/toggle-adoption-status', methods=['PUT'])
@admin_required
def toggle_adoption_status(id):
    animal = Animal.find_by_id(id)

    if not animal:
        return {"error": "Animal not found"}, 404

    Animal.toggle_adoption_status(id)
    
    return "success"
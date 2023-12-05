from flask import Blueprint, redirect, render_template, request, url_for, session, request
from flask_login import current_user

from ...models import Animal, Adoption, Notification
from ...utils import admin_required, get_active_filter_count
from ...validations import AddAnimalValidation, EditAnimalValidation
from ...enums import NotificationType
 
admin_animal_bp = Blueprint("animals", __name__, url_prefix='/animals')

@admin_animal_bp.route('', methods=['GET'])
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
        page_size=12,
        filters=filters
    )

    animals = animals_query.get("data")
    has_previous_page = animals_query.get("has_previous_page")
    has_next_page = animals_query.get("has_next_page")
    total_count = animals_query.get("total_count")

    return render_template('admin/animal/animals.html', 
                            animals=animals,
                            has_previous_page=has_previous_page,
                            has_next_page=has_next_page,
                            total_count=total_count,
                            filters=filters,
                            active_filters=get_active_filter_count(filters),
                            view_type=view_type
                        )

@admin_animal_bp.route('/<int:id>', methods=['GET'])
@admin_required
def view_animal(id):
  animal = Animal.find_by_id(id)
  return render_template('/admin/animal/animal.html', animal=animal)  
  
@admin_animal_bp.route('/add-animal', methods=['GET', 'POST'])
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
    is_adopted = form.is_adopted.data
    is_dead = form.is_dead.data
    is_dewormed = form.is_dewormed.data
    is_neutered = form.is_neutered.data
    in_shelter = form.in_shelter.data
    is_rescued = form.is_rescued.data
    for_adoption = form.for_adoption.data
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
      for_adoption=for_adoption,
      description=description,
      appearance=appearance,
      author_id=author_id
    )

    if animal_id:
       return redirect(url_for('admin.animals.animals'))


  return render_template('admin/animal/add.html', form=form)

@admin_animal_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
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
        animal.is_adopted = form.is_adopted.data
        animal.is_dead = form.is_dead.data
        animal.is_dewormed = form.is_dewormed.data
        animal.is_neutered = form.is_neutered.data
        animal.in_shelter = form.in_shelter.data
        animal.is_rescued = form.is_rescued.data
        animal.for_adoption = form.for_adoption.data
        animal.description = form.description.data
        animal.appearance = form.appearance.data

        Animal.edit(animal)
        
        return redirect(url_for("admin.animals.animals"))
    
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
        form.is_adopted.data = animal.is_adopted == 1
        form.is_dead.data = animal.is_dead == 1
        form.is_dewormed.data = animal.is_dewormed == 1
        form.is_neutered.data = animal.is_neutered == 1
        form.in_shelter.data = animal.in_shelter == 1
        form.is_rescued.data = animal.is_rescued == 1
        form.for_adoption.data = animal.for_adoption == 1
            
    return render_template('admin/animal/edit.html', form=form)

@admin_animal_bp.route('/<int:id>/delete', methods=['DELETE'])
@admin_required
def delete_animal(id):
    animal = Animal.find_by_id(id)

    if not animal:
        return {"error": "Animal not found"}, 404

    Animal.delete(id)
    
    return True

@admin_animal_bp.route('/adoptions', methods=['GET'])
@admin_required
def adoptions():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query', '', type=str)

    animals = Adoption.get_animals_applications()
    return render_template('/admin/animal/adoptions.html', animals=animals)


@admin_animal_bp.route('/adoptions/<int:id>', methods=['GET'])
@admin_required
def adoption(id):
    animal = Animal.find_by_id(id)
    applications = Adoption.get_animal_applications(id)
    return render_template('admin/animal/adoption.html', animal=animal, applications=applications)

@admin_animal_bp.route('/adoptions/<int:animal_id>/under-review', methods=['POST'])
@admin_required
def set_under_review(animal_id):
    remarks = request.form.get('remarks')
    user_id = request.form.get('user_id')
    adoption_id = request.form.get('adoption_id')

    Adoption.set_under_review(adoption_id=adoption_id, user_id=user_id, remarks=remarks)
    notification = Notification(type=NotificationType.ADOPTION_STATUS_UPDATE.value, animal_id=animal_id, adoption_id=adoption_id, user_who_fired_event_id=1, user_to_notify_id=user_id)
    notification.insert(notification)
    notification.increment_count(notification)
    return redirect(url_for('admin.animals.adoption', id=id))

@admin_animal_bp.route('/adoptions/<int:animal_id>/approve', methods=['POST'])
@admin_required
def set_approved(id, user_id):
    Adoption.set_approved_and_reject_others(animal_id=id, user_id=user_id)
    notification = Notification(type=NotificationType.ADOPTION_STATUS_UPDATE.value,  adoption_id=id, user_who_fired_event_id=1, user_to_notify_id=user_id)
    notification.insert(notification)
    notification.increment_count(notification)
    return redirect(url_for('admin.animals.adoption', id=id))

@admin_animal_bp.route('/adoptions/<int:animal_id>/turnover', methods=['POST'])
@admin_required
def set_turnovered(id, user_id):
    Adoption.set_turnovered(animal_id=id, user_id=user_id)
    notification = Notification(type=NotificationType.ADOPTION_STATUS_UPDATE.value,  adoption_id=id, user_who_fired_event_id=1, user_to_notify_id=user_id)
    notification.insert(notification)
    notification.increment_count(notification)
    return redirect(url_for('admin.animals.adoption', id=id))

@admin_animal_bp.route('/adoptions/<int:animal_id>/reject', methods=['POST'])
@admin_required
def set_rejected(id, user_id):
    Adoption.set_rejected(animal_id=id, user_id=user_id)
    notification = Notification(type=NotificationType.ADOPTION_STATUS_UPDATE.value,  adoption_id=id, user_who_fired_event_id=1, user_to_notify_id=user_id)
    notification.insert(notification)
    notification.increment_count(notification)
    return redirect(url_for('admin.animals.adoption', id=id))

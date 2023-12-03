from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)
from flask_login import current_user

from ...models import AdoptionApplication, Animal
from ...utils import get_active_filter_count, user_verified_required
from ...validations import AdoptApplicationValidation

user_animal_bp = Blueprint("animals", __name__, url_prefix='/animals')

@user_animal_bp.route('', methods=['GET'])
@user_verified_required
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

    return render_template('user/animals/animals.html', 
                            animals=animals,
                            page_number=page,
                            has_previous_page=has_previous_page,
                            has_next_page=has_next_page,
                            total_count=total_count,
                            filters=filters,
                            active_filters=get_active_filter_count(filters),
                            view_type=view_type
                            )

@user_animal_bp.route('/<int:id>', methods=['GET'])
@user_verified_required
def view_animal(id):
  animal = Animal.find_by_id(id)
  return render_template('/user/animals/animal.html', animal=animal)  

@user_animal_bp.route('/adoptions', methods=['GET'])
@user_verified_required
def adoptions():
    page = request.args.get('page', 1, type=int)
    view_type = session.get('view_type')

    filters = {
        'query': request.args.get('query', '', type=str),
        'for_adoption': True,
        'is_dead': False,
    }

    animals_query = Animal.find_all_adoptions(
        page_number=page,
        page_size=12,
        filters=filters,
        user_id=current_user.id
    )

    animals = animals_query.get("data")
    has_previous_page = animals_query.get("has_previous_page")
    has_next_page = animals_query.get("has_next_page")
    total_count = animals_query.get("total_count")

    return render_template('user/animals/adoptions.html', 
                            animals=animals,
                            page_number=page,
                            has_previous_page=has_previous_page,
                            has_next_page=has_next_page,
                            total_count=total_count,
                            filters=filters,
                            active_filters=get_active_filter_count(filters),
                            view_type=view_type
                            )

@user_animal_bp.route('/adoptions/<int:id>', methods=['GET', 'POST'])
@user_verified_required
def adopt_me(id):
  animal = Animal.find_by_id(id)
  active_application = AdoptionApplication.find_by_user_animal(user_id=current_user.id, animal_id=animal.id)

  form = AdoptApplicationValidation()

  if form.validate_on_submit():
    new_application = AdoptionApplication(user_id=current_user.id,
                                          animal_id=animal.id, 
                                          reason_to_adopt=form.reason_to_adopt.data, 
                                          interview_type_preference=form.interview_type_preference.data, 
                                          interview_preferred_date=form.interview_preferred_date.data, 
                                          interview_preferred_time=form.interview_preferred_time.data)
    if active_application: 
      new_application.update(new_application)
    else:
      new_application.insert(new_application)

    return redirect(url_for('user.applications'))

  if not form.is_submitted() and active_application:
     form.id.data = active_application.id
     form.reason_to_adopt.data = active_application.reason_to_adopt  
     form.interview_type_preference.data = active_application.interview_type_preference   
     form.interview_preferred_date.data = active_application.interview_preferred_date  
     form.interview_preferred_time.data = active_application.interview_preferred_time  
  
  return render_template('/user/animals/adopt_me.html', animal=animal, active_application=active_application, form=form)

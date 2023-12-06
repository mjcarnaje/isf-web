from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)
from flask_login import current_user

from ...models import Adoption, Animal, Notification
from ...utils import get_active_filter_count, user_verified_required
from ...validations import AdoptionValidation
from ...enums import NotificationType

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
  active_application = Adoption.find_by_user_animal(user_id=current_user.id, animal_id=animal.id)

  form = AdoptionValidation()

  if form.validate_on_submit():
    application = Adoption(
                        user_id=current_user.id,
                        animal_id=animal.id, 
                        reason_to_adopt=form.reason_to_adopt.data, 
                        interview_preference=form.interview_preference.data, 
                        interview_preferred_date=form.interview_preferred_date.data, 
                        phone_number=form.phone_number.data,
                        interview_preferred_time=form.interview_preferred_time.data
                      )
    if active_application: 
      application.update(application)
    else:
      application_id =  application.insert(application)
      notification = Notification(
                              type=NotificationType.ADOPTION_REQUEST.value,
                              animal_id=animal.id,
                              adoption_id=application_id,
                              user_who_fired_event_id=current_user.id,
                              user_to_notify_id=1
                            )
      notification.insert(notification)
      notification.increment_count(notification)

    return redirect(url_for('user.applications'))

  if not form.is_submitted() and active_application:
    form.id.data = active_application.id
    form.reason_to_adopt.data = active_application.reason_to_adopt  
    form.phone_number.data = active_application.phone_number
    form.interview_preference.data = active_application.interview_preference   
    form.interview_preferred_date.data = active_application.interview_preferred_date  
    form.interview_preferred_time.data = active_application.interview_preferred_time  
  else:
    form.phone_number.data = current_user.contact_number

  
  return render_template('/user/animals/adopt_me.html', animal=animal, active_application=active_application, form=form)

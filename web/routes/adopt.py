from flask import Blueprint, render_template, request, redirect, url_for

from ..models import Animal, AdoptionApplication
from ..utils import user_only
from ..validations import AdoptApplicationValidation
from flask_login import current_user, login_required

adopt_bp = Blueprint("adopt", __name__, url_prefix='/adopt')

@adopt_bp.route('/', methods=['GET'])
@user_only
def index():
  page = request.args.get('page', 1, type=int)
  animals_query = Animal.find_all(
              page_number=page, 
              page_size=12,
              filters={
                'for_adoption': True
              }
            )
  
  animals = animals_query.get("data")
  has_previous_page = animals_query.get("has_previous_page")
  has_next_page = animals_query.get("has_next_page")
  total_count = animals_query.get("total_count")
  
  return render_template('/landing/adopt/adopts.html',  animals=animals, page_number=page, has_previous_page=has_previous_page, has_next_page=has_next_page, total_count=total_count)


@adopt_bp.route('/<int:id>', methods=['GET', 'POST'])
@login_required
@user_only
def adopt_me(id):
  animal = Animal.find_by_id(id)

  form = AdoptApplicationValidation()

  if form.validate_on_submit():
    new_application = AdoptionApplication(user_id=current_user.id,
                                          animal_id=animal.id, 
                                          reason_to_adopt=form.reason_to_adopt.data, 
                                          interview_type_preference=form.interview_type_preference.data, 
                                          interview_preferred_date=form.interview_preferred_date.data, 
                                          interview_preferred_time=form.interview_preferred_time.data)
    new_application.insert(new_application)
    redirect(url_for('user.applications'))
  
  active_application = AdoptionApplication.find_by_user_animal(user_id=current_user.id, animal_id=animal.id)
  
  return render_template('/landing/adopt/adopt.html', animal=animal, active_application=active_application, form=form)


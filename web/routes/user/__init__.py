from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, logout_user

from ...models import AdoptionApplication, Donation, Animal
from ...utils import user_verified_required

from ...validations import AdoptApplicationValidation

user_bp = Blueprint("user", __name__, url_prefix='/user')

@user_bp.route('/', methods=['GET', 'POST'])
@user_verified_required
def index():
  return redirect(url_for('user.dashboard'))

@user_bp.route('/dashboard', methods=['GET', 'POST'])
@user_verified_required
def dashboard():
  return render_template('user/dashboard.html')

@user_bp.route('/animals/adoptions/adopt/<int:id>', methods=['GET', 'POST'])
@user_verified_required
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


@user_bp.route('/donations', methods=['GET', 'POST'])
@user_verified_required
def donations():
  donations = Donation.get_user_donations(current_user.id)
  return render_template('user/donations.html', donations=donations)

@user_bp.route('/applications', methods=['GET', 'POST'])
@user_verified_required
def applications():
  applications = AdoptionApplication.get_user_applications(current_user.id)
  return render_template('user/applications.html', applications=applications)

@user_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('landing.index'))


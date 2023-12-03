from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, logout_user

from ...models import AdoptionApplication, Donation
from ...utils import user_verified_required

from .animal import user_animal_bp

user_bp = Blueprint("user", __name__, url_prefix='/user')

@user_bp.route('/', methods=['GET', 'POST'])
@user_verified_required
def index():
  return redirect(url_for('user.dashboard'))

@user_bp.route('/dashboard', methods=['GET', 'POST'])
@user_verified_required
def dashboard():
  return render_template('user/dashboard.html')

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


user_bp.register_blueprint(user_animal_bp)
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from ...models import User, UserRole, Donation
from ...validations import UserLoginValidation, UserSignupValidation
from ...utils import user_only

user_bp = Blueprint("user", __name__, url_prefix='/user')

@user_bp.route('/dashboard', methods=['GET', 'POST'])
@user_only
def dashboard():
  return render_template('user/dashboard.html')

@user_bp.route('/donations', methods=['GET', 'POST'])
@user_only
def donations():
  donations = Donation.get_user_donations(current_user.id)
  return render_template('user/donations.html', donations=donations)

@user_bp.route('/login', methods=['GET', 'POST'])
@user_only
def login():
  form = UserLoginValidation()

  if form.validate_on_submit():
    user = User.find_by_username(username=form.username.data)

    if user and check_password_hash(user.password, form.password.data):
      login_user(user, remember=True)
      
      next_page = request.args.get("next")

      if next_page:
         return redirect(next_page)
      
      return redirect(url_for('landing.index'))

     
  return render_template('user/login.html', form=form)


@user_bp.route("/sign-up", methods=['POST', 'GET'])
@user_only
def sign_up():
  form = UserSignupValidation()
  
  if form.validate_on_submit():
    new_user = User(
      email=form.email.data,
      username=form.username.data,
      first_name=form.first_name.data,
      last_name=form.last_name.data,
      photo_url=form.photo_url.data,
      contact_number=form.contact_number.data,
      password=generate_password_hash(form.password.data),
    )

    user_id = User.insert(new_user)
    UserRole.insert_user_role_by_name(user_id=user_id, role_name="member")
    
    return redirect(url_for('user.login'))


  return render_template('user/sign_up.html', form=form)

@user_bp.route("/logout")
@user_only
def logout():
    logout_user()
    return redirect(url_for('landing.index'))


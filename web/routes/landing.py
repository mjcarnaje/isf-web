from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required, login_user
from werkzeug.security import check_password_hash, generate_password_hash

from ..models import (AdoptionApplication, Animal, Donation, Event, User,
                      UserRole)
from ..utils import (anonymous_required, check_verification_token,
                     generate_verification_token, send_verification_email,
                     user_verified_required)
from ..validations import (AddDonation_In_Kind, AddDonationMoney,
                           NewEmailValidation, UserLoginValidation,
                           UserSignupValidation)

landing_bp = Blueprint("landing", __name__)

@landing_bp.route('/', methods=['GET'])
@anonymous_required
def index():
  animals_query = Animal.find_all(
      page_number=1,
      page_size=6,
  )
  return render_template('/landing/home.html', animals=animals_query.get('data'))
  
@landing_bp.route('/about-us')
def about_us():
    return render_template('/landing/about_us.html')

@landing_bp.route('/adopt', methods=['GET'])
@anonymous_required
def adopt():
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

@landing_bp.route('/recues', methods=['GET'])
@anonymous_required
def animals():
  page = request.args.get('page', 1, type=int)
  animals_query = Animal.find_all(
              page_number=page, 
              page_size=12
            )
  
  animals = animals_query.get("data")
  has_previous_page = animals_query.get("has_previous_page")
  has_next_page = animals_query.get("has_next_page")
  total_count = animals_query.get("total_count")
  
  return render_template('/landing/rescue/rescues.html',  animals=animals, page_number=page, has_previous_page=has_previous_page, has_next_page=has_next_page, total_count=total_count)

@landing_bp.route('/<int:id>', methods=['GET'])
@anonymous_required
def view_animal(id):
  animal = Animal.find_by_id(id)
  return render_template('/landing/rescue/rescue.html', animal=animal)

@landing_bp.route('/donate', methods=['GET'])
@anonymous_required
def donate():
  return render_template('/landing/donate/donate.html')


@landing_bp.route('/money', methods=['GET', 'POST'])
def donate_money():
  form = AddDonationMoney()
    
  if form.validate_on_submit():
    new_donation = Donation(
      remarks=form.remarks.data,
      amount=form.amount.data,
      pictures=form.pictures.data,
      donation_type='money',
      type='org',
      user_id=current_user.id
    )
    Donation.insert(new_donation)
    return redirect(url_for('user.dashboard'))

  return render_template('/landing/donate/donate_money.html', form=form)


@landing_bp.route('/in-kind', methods=['GET', 'POST'])
@user_verified_required
def donate_in_kind():
  form = AddDonation_In_Kind()
    
  if form.validate_on_submit():
    new_donation = Donation(
      remarks=form.remarks.data,
      pictures=form.pictures.data,
      delivery_type=form.delivery_type.data,
      pick_up_location=form.pick_up_location.data,
      donation_type='in_kind',
      type='org',
      user_id=current_user.id
    )
    Donation.insert(new_donation)
    return redirect(url_for('user.dashboard'))
  
  return render_template('/landing/donate/landing.donate_in_kind.html', form=form)
   
@landing_bp.route('/events', methods=['GET'])
@anonymous_required
def events():
  events = Event.find_all(show_landing_page_only=True)
  return render_template('/landing/event/events.html', events=events.get('data'))

@landing_bp.route('/events/<int:id>', methods=['GET'])
@anonymous_required
def view_event(id):
  event = Event.find_by_id(event_id=id)
  return render_template('/landing/event/event.html', event=event)

@landing_bp.route('/volunteers', methods=['GET'])
@anonymous_required
def volunteers():
  return render_template('/landing/volunteer/volunteer.html')

@landing_bp.route('/verify-account', methods=['GET', 'POST'])
@login_required
def verify_account():
    token = request.args.get('token')

    if current_user.is_verified:
      return redirect(url_for('user.index'))
    
    if token:
        token = check_verification_token(token)

        if token.get('is_valid'):
          User.set_is_verified(current_user.id)
          return render_template('/landing/verify_account.html', is_valid=True)
        
        if token.get('is_expired'):
          return render_template('/landing/verify_account.html', is_expired=True)
    
    if request.method == 'POST':
        current_app.logger.info('Requesting another token..')
        token = generate_verification_token(user_id=current_user.id, email=current_user.email)
        send_verification_email(email=current_user.email, token=token, user=current_user)
        flash('Email is sent!', 'success')
      
    return render_template('/landing/verify_account.html', is_expired=False)

@landing_bp.route('/enter-new-email', methods=['GET', 'POST'])
@login_required
def enter_new_email():
    if current_user.is_verified:
      return redirect(url_for('user.index'))

    form = NewEmailValidation()
    
    form.id.data = current_user.id
    form.old_email.data = current_user.email

    if form.validate_on_submit():
      user_id = current_user.id
      new_email = form.email.data
      User.update_email(email=new_email, user_id=user_id)
      token = generate_verification_token(user_id=user_id, email=new_email)
      send_verification_email(email=new_email, token=token, user=current_user)

      flash('Successfuly update your email', 'success')
      return redirect(url_for('landing.verify_account'))

    return render_template('/landing/enter_new_email.html', form=form)


@landing_bp.route('/login', methods=['GET', 'POST'])
@anonymous_required
def login():
  form = UserLoginValidation()

  if form.validate_on_submit():
    user = User.find_by_username(username=form.username.data)

    if user and check_password_hash(user.password, form.password.data):
      login_user(user, remember=True)
      
      next_page = request.args.get("next")

      if next_page:
         return redirect(next_page)
      
      return redirect(url_for('user.index'))

     
  return render_template('user/login.html', form=form)
  

@landing_bp.route("/sign-up", methods=['POST', 'GET'])
@anonymous_required
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
    token = generate_verification_token(user_id=user_id, email=new_user.email)
    send_verification_email(email=new_user.email, token=token, user=new_user)

    flash('Check your email to confirm your account.', 'success')

    return redirect(url_for('landing.login'))


  return render_template('user/sign_up.html', form=form)


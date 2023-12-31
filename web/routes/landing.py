from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, session, url_for)
from flask_login import current_user, login_required, login_user
from werkzeug.security import check_password_hash, generate_password_hash

from ..config import Config
from ..models import Animal, Event, User, EventPost
from ..utils import (anonymous_required, check_verification_token,
                     generate_verification_token, get_active_filter_count,
                     send_verification_email, pagination)
from ..validations import (NewEmailValidation, UserLoginValidation,
                           UserSignupValidation)

landing_bp = Blueprint("landing", __name__)

@landing_bp.route('/', methods=['GET'])
@anonymous_required
def index():
  animals_query = Animal.find_all(
      page_number=1,
      page_size=Config.DEFAULT_PAGE_SIZE,
      filters={
         'is_dead': 0
      }
  )
  return render_template('/landing/home.html', animals=animals_query.get('data'))
  
@landing_bp.route('/about-us')
def about_us():
    return render_template('/landing/about_us.html')

@landing_bp.route('/adopt', methods=['GET'])
@anonymous_required
def adopt():
  page = request.args.get('page', 1, type=int)
  view_type = session.get('view_type')

  filters = {
    'query': request.args.get('query', '', type=str),
    'for_adoption': True, 
  }
  
  animals_query = Animal.find_all(
              page_number=page, 
              page_size=Config.DEFAULT_PAGE_SIZE,
              filters=filters
            )
  
  animals = animals_query.get("data")
  total_count = animals_query.get("total_count")
  offset = animals_query.get("offset")
  
  return render_template('/landing/adopt/adopts.html',
      animals=animals, 
      filters=filters,
      active_filters=get_active_filter_count(filters),
      view_type=view_type,
      pagination = pagination(
        page_number=page,
        offset=offset,
        page_size=Config.DEFAULT_PAGE_SIZE,
        total_count=total_count,
        base_url="landing.adopt"
      )
  )

@landing_bp.route('/recues', methods=['GET'])
@anonymous_required
def animals():
  page = request.args.get('page', 1, type=int)
  view_type = session.get('view_type')
  
  filters = {
      'query': request.args.get('query', '', type=str),
      'is_dead': 0
  }

  
  animals_query = Animal.find_all(
              page_number=page, 
              page_size=Config.DEFAULT_PAGE_SIZE,
              filters=filters
            )
  
  animals = animals_query.get("data")
  total_count = animals_query.get("total_count")
  offset = animals_query.get("offset")
  
  return render_template('/landing/rescue/rescues.html', 
            animals=animals, 
            filters=filters,
            active_filters=get_active_filter_count(filters),
            view_type=view_type,
            pagination = pagination(
              page_number=page,
              offset=offset,
              page_size=Config.DEFAULT_PAGE_SIZE,
              total_count=total_count,
              base_url="landing.animals"
            )
          )

@landing_bp.route('/<int:id>', methods=['GET'])
@anonymous_required
def view_animal(id):
  animal = Animal.find_one(id)
  return render_template('/landing/rescue/rescue.html', animal=animal)

@landing_bp.route('/donate', methods=['GET'])
@anonymous_required
def donate():
  return render_template('/landing/donate/donate.html')

@landing_bp.route('/events', methods=['GET'])
@anonymous_required
def events():
  events = Event.find_all(page_number=1, page_size=12, filters={
     'who_can_see_it': 'Public'
  })

  return render_template('/landing/event/events.html', events=events.get('data'))

@landing_bp.route('/events/<int:id>', methods=['GET'])
@anonymous_required
def view_event(id):
  event = Event.find_one(event_id=id)
  statistics = Event.get_statistics(id)
  posts = EventPost.find_posts(event_id=id)
  return render_template('/landing/event/event.html', event=event, posts=posts, statistics=statistics)

@landing_bp.route('/volunteers', methods=['GET'])
@anonymous_required
def volunteers():
  members = User.find_members()
  return render_template('/landing/volunteer/volunteer.html', members=members)

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
      if not Config.IS_MAIL_TRAP_AVAILABLE:
        flash('Our Email Provider is not available.')
      else:
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
        gender=form.gender.data,
        contact_number=form.contact_number.data,
        password=generate_password_hash(form.password.data),
      )

      user_id = User.insert(new_user)
      token = generate_verification_token(user_id=user_id, email=new_user.email)

      if Config.IS_MAIL_TRAP_AVAILABLE:
        send_verification_email(email=new_user.email, token=token, user=new_user)
        flash('Check your email to confirm your account.', 'success')
      else:
        User.set_is_verified(user_id=user_id)
        flash('You are verified!')

      return redirect(url_for('landing.login'))

  return render_template('user/sign_up.html', form=form)


@landing_bp.route("/set_view_type/<string:view_type>", methods=['POST'])
def set_view_type(view_type):
  session['view_type'] = view_type
  current_app.logger.info("Done setting view type")
  return 'ok'


from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from flask_login import current_user, logout_user
from ...config import Config

from ...models import Adoption, Donation, Notification, NotificationSettings, Event, User, MemberApplication
from ...utils import user_verified_required, get_active_filter_count, pagination

from .animal import user_animal_bp
from .event import user_event_bp
from .donation import user_donation_bp
from .adoption import user_adoption_bp
from .application import user_application_bp
from ...validations import NotificationSettingsValidation, EditProfileValidation, MemberApplicationValidation
from ...enums import NotificationType

user_bp = Blueprint("user", __name__, url_prefix='/user')

@user_bp.route('/', methods=['GET', 'POST'])
@user_verified_required
def index():
  return redirect(url_for('user.dashboard'))

@user_bp.route('/dashboard', methods=['GET', 'POST'])
@user_verified_required
def dashboard():
  latest_event = Event.get_latest_event()
  featured_events = Event.get_featured()
  return render_template('user/dashboard.html', latest_event=latest_event, featured_events=featured_events)

@user_bp.route('/notifications', methods=['GET'])
@user_verified_required
def notifications(): 
  notifications = Notification.find_all(
      page_number=1,
      page_size=Config.DEFAULT_PAGE_SIZE,
      filters={
         'user_to_notify_id': current_user.id,
         'is_archived': 0
      }
   )
  return render_template('/user/notifications.html', notifications=notifications)

@user_bp.route('/notifications/mark-as-read/<id>', methods=['PUT'])
@user_verified_required
def mark_as_read_notification(id):
   Notification.mark_as_read(notification_id=id, user_id=current_user.id)
   return "success"

@user_bp.route('/notifications/mark-as-archived/<id>', methods=['PUT'])
@user_verified_required
def mark_as_archived_notification(id):
   Notification.mark_as_archived(notification_id=id, user_id=current_user.id)
   return "success"

@user_bp.route('/notifications/mark-all-as-read', methods=['PUT'])
@user_verified_required
def mark_all_as_read_notification():
   Notification.mark_all_as_read(user_id=current_user.id)
   return "success"

@user_bp.route('/donations', methods=['GET', 'POST'])
@user_verified_required
def donations():
  page = request.args.get('page', 1, type=int)
  view_type = session.get('view_type')

  filters = {
    'user_id': current_user.id,
    'donation_type': request.args.get('donation_type')
  }
  
  donations_query = Donation.find_all(
      page_number=page,
      page_size=Config.DEFAULT_PAGE_SIZE,
      filters=filters
  )

  donations = donations_query.get("data")
  total_count = donations_query.get("total_count")
  offset = donations_query.get("offset")
    
  return render_template('user/donations.html',
    donations=donations,
    filters=filters,
    active_filters=get_active_filter_count(filters, ["user_id"]),
    view_type=view_type,
    pagination = pagination(
        page_number=page,
        offset=offset,
        page_size=Config.DEFAULT_PAGE_SIZE,
        total_count=total_count,
        base_url="user.donations"
    ),
  )

@user_bp.route('/settings', methods=['GET', 'POST'])
@user_verified_required
def settings():
  return redirect(url_for('user.account_settings'))
  
@user_bp.route('/settings/accounts', methods=['GET', 'POST'])
@user_verified_required
def account_settings():
  form = EditProfileValidation()

  if form.validate_on_submit():
    edited_user = User(
      id=form.id.data,
      email=current_user.email,
      username=form.username.data,
      first_name=form.first_name.data,
      last_name=form.last_name.data,
      photo_url=form.photo_url.data,
      contact_number=form.contact_number.data,
    )
    edited_user.update(edited_user)
    
    return redirect(url_for('user.account_settings'))

  if not form.is_submitted():
      form.id.data = current_user.id
      form.username.data = current_user.username
      form.first_name.data = current_user.first_name
      form.last_name.data = current_user.last_name
      form.photo_url.data = current_user.photo_url
      form.contact_number.data = current_user.contact_number

  return render_template('user/settings/account.html', form=form)

@user_bp.route('/settings/notifications', methods=['GET', 'POST'])
@user_verified_required
def notifications_settings():
  form = NotificationSettingsValidation()

  if form.validate_on_submit():
    NotificationSettings.update_notification_settings(
      user_id=current_user.id, 
      
      adoption_status_update_web=form.adoption_status_update_web.data,
      donation_status_update_web=form.donation_status_update_web.data,
      event_invited_web=form.event_invited_web.data,
      confirm_join_org_request_web=form.confirm_join_org_request_web.data,
      reject_join_org_request_web=form.reject_join_org_request_web.data,

      adoption_status_update_email=form.adoption_status_update_email.data,
      donation_status_update_email=form.donation_status_update_email.data,
      event_invited_email=form.event_invited_email.data,
      confirm_join_org_request_email=form.confirm_join_org_request_email.data,
      reject_join_org_request_email=form.reject_join_org_request_email.data
    )
    flash("Notification settings saved.", "success")

  notification_settings = NotificationSettings.find_one(user_id=current_user.id)

  form.adoption_status_update_web.data = notification_settings['adoption_status_update_web'] == 1
  form.donation_status_update_web.data = notification_settings['donation_status_update_web'] == 1
  form.event_invited_web.data = notification_settings['event_invited_web'] == 1
  form.confirm_join_org_request_web.data = notification_settings['confirm_join_org_request_web'] == 1
  form.reject_join_org_request_web.data = notification_settings['reject_join_org_request_web'] == 1

  form.adoption_status_update_email.data = notification_settings['adoption_status_update_email'] == 1
  form.donation_status_update_email.data = notification_settings['donation_status_update_email'] == 1
  form.event_invited_email.data = notification_settings['event_invited_email'] == 1
  form.confirm_join_org_request_email.data = notification_settings['confirm_join_org_request_email'] == 1
  form.reject_join_org_request_email.data = notification_settings['reject_join_org_request_email'] == 1
  
  return render_template('user/settings/notifications.html', form=form)

@user_bp.route('view-profile')
@user_verified_required
def view_profile():
  return render_template('user/view_profile.html')

@user_bp.route('be-a-member', methods=['GET', 'POST'])
@user_verified_required
def be_a_member():
  form = MemberApplicationValidation()

  if form.validate_on_submit():
    member_application = MemberApplication(user_id=current_user.id, join_reason=form.join_reason.data)
    member_application_id = member_application.insert(member_application)
    print(member_application_id)
    notification = Notification(
      type=NotificationType.JOIN_ORG_REQUEST.value,
      member_application_id=member_application_id,
      user_who_fired_event_id=current_user.id,
      user_to_notify_id=1
    )
    Notification.insert_multiple([notification])
    flash("You have sumbitted your application!", "success")
  
  existing_application = MemberApplication.find_by_user_id(current_user.id)

  return render_template('user/be_a_member.html', form=form, existing_application=existing_application)

@user_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('landing.index'))


user_bp.register_blueprint(user_animal_bp)
user_bp.register_blueprint(user_event_bp)
user_bp.register_blueprint(user_donation_bp)
user_bp.register_blueprint(user_adoption_bp)
user_bp.register_blueprint(user_application_bp)
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash

from ...models import Animal, Notification, User
from ...utils import admin_required
from ...validations import AdminLoginValidation

admin_bp = Blueprint("admin", __name__, url_prefix='/admin')

from .adoption import adoption_bp
from .animal import animal_bp
from .donation import donations_bp
from .event import event_bp

admin_bp.register_blueprint(animal_bp)
admin_bp.register_blueprint(event_bp)
admin_bp.register_blueprint(donations_bp)
admin_bp.register_blueprint(adoption_bp)

@admin_bp.route('/', methods=['GET'])
@admin_required
def index(): 
   animal_stats = Animal.get_stats()
   return render_template('/admin/dashboard.html', animal_stats=animal_stats)

@admin_bp.route('/notifications', methods=['GET'])
@admin_required
def notifications(): 
   notifications = Notification.get_notifications(user_id=current_user.id, limit=10)
   return render_template('/admin/notifications.html', notifications=notifications)

@admin_bp.route('/notifications/mark-as-read/<int:id>', methods=['PUT'])
@admin_required
def mark_as_read_notifcation(id):
   Notification.mark_as_read(notification_id=id, user_id=current_user.id)
   return "success"

@admin_bp.route('/notifications/mark-all-as-read', methods=['PUT'])
@admin_required
def mark_all_as_read_notification():
   Notification.mark_all_as_read(user_id=current_user.id)
   return "success"

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
  form = AdminLoginValidation()

  if form.validate_on_submit():
    admin = User.find_by_username(username=form.username.data)

    if admin and check_password_hash(admin.password, form.password.data):
      login_user(admin, remember=True)
      
      next_page = request.args.get("next")

      if next_page:
         return redirect(next_page)
      
      return redirect(url_for('landing.index'))

     
  return render_template('admin/login.html', form=form)


@admin_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('landing.index'))
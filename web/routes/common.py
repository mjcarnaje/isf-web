
from flask import Blueprint
from flask_login import current_user, login_required

from ..models import Notification

common_bp = Blueprint("common", __name__, url_prefix='/')


@common_bp.route('/notifications/mark-as-read/<id>', methods=['PUT'])
@login_required
def mark_as_read_notification(id):
   Notification.mark_as_read(notification_id=id, user_id=current_user.id)
   return "success"

@common_bp.route('/notifications/mark-as-archived/<id>', methods=['PUT'])
@login_required
def mark_as_archived_notification(id):
   Notification.mark_as_archived(notification_id=id, user_id=current_user.id)
   return "success"

@common_bp.route('/notifications/mark-all-as-read', methods=['PUT'])
@login_required
def mark_all_as_read_notification():
   Notification.mark_all_as_read(user_id=current_user.id)
   return "success"
from flask import (Blueprint, render_template, request, session, flash)

from ...config import Config
from ...models import MemberApplication, Notification
from ...utils import admin_required, get_active_filter_count
from ...utils import pagination
from ...enums import NotificationType
from flask_login import current_user

member_application_bp = Blueprint("member_application", __name__, url_prefix='/member-applications')

@member_application_bp.route('', methods=['GET'])
@admin_required
def member_applications():
    page = request.args.get('page', 1, type=int)
    view_type = session.get('view_type')

    filters = {
        'query': request.args.get('query', '', type=str),
        'gender': request.args.get('gender', '')
    }

    users_query = MemberApplication.find_all(
        page_number=page,
        page_size=Config.DEFAULT_PAGE_SIZE,
        filters=filters
    )

    users = users_query.get("data")
    total_count = users_query.get("total_count")
    offset = users_query.get("offset")

    return render_template('admin/member-application/member_applications.html', 
        users=users,
        filters=filters,
        active_filters=get_active_filter_count(filters),
        view_type=view_type,
        pagination = pagination(
            page_number=page,
            offset=offset,
            page_size=Config.DEFAULT_PAGE_SIZE,
            total_count=total_count,
            base_url="admin.member_application.member_applications"
        ),
    )

@member_application_bp.route('/<int:id>', methods=['GET'])
@admin_required
def view_member_application(id):
  user = MemberApplication.find_by_id(id)
  return render_template('/admin/member-application/member_applications.html', user=user)  


@member_application_bp.route("/<id>/delete", methods=['DELETE'])
@admin_required
def delete_member_application(id):
   MemberApplication.delete(id)
   flash("Successfuly delete user.", "success")
   return "success"
   
@member_application_bp.route("/<id>/reject", methods=['PUT'])
@admin_required
def reject_member_application(id):
    MemberApplication.reject(id)
    notification = Notification(
      type=NotificationType.REJECT_JOIN_ORG_REQUEST.value,
      member_application_id=id,
      user_who_fired_event_id=current_user.id,
      user_to_notify_id=request.args.get('user_id')
    )
    notification.insert_multiple([notification])
    flash("Successfuly reject user.", "success")
    return "success"

@member_application_bp.route("/<id>/confirm", methods=['PUT'])
@admin_required
def confirm_member_application(id):
    MemberApplication.confirm(id)
    notification = Notification(
        type=NotificationType.CONFIRM_JOIN_ORG_REQUEST.value,
        member_application_id=id,
        user_who_fired_event_id=current_user.id,
        user_to_notify_id=request.args.get('user_id')
    )
    notification.insert_multiple([notification])
    flash("Successfuly confirm user.", "success")
    return "success"
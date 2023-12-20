from flask import (Blueprint, render_template, request, session, flash)

from ...config import Config
from ...models import User
from ...utils import admin_required, get_active_filter_count
from ...utils import pagination

user_bp = Blueprint("user", __name__, url_prefix='/users')

@user_bp.route('', methods=['GET'])
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    view_type = session.get('view_type')

    filters = {
        'query': request.args.get('query', '', type=str),
        'gender': request.args.get('gender', ''),
        'role_name': request.args.get('role', '')
    }

    users_query = User.find_all(
        page_number=page,
        page_size=Config.DEFAULT_PAGE_SIZE,
        filters=filters
    )

    users = users_query.get("data")
    total_count = users_query.get("total_count")
    offset = users_query.get("offset")

    return render_template('admin/user/users.html', 
        users=users,
        filters=filters,
        active_filters=get_active_filter_count(filters),
        view_type=view_type,
        pagination = pagination(
            page_number=page,
            offset=offset,
            page_size=Config.DEFAULT_PAGE_SIZE,
            total_count=total_count,
            base_url="admin.user.users"
        ),
    )

@user_bp.route('/<int:id>', methods=['GET'])
@admin_required
def view_user(id):
  user = User.find_by_id(id)
  return render_template('/admin/user/user.html', user=user)  


@user_bp.route("/<int:id>/delete", methods=['DELETE'])
@admin_required
def delete_user(id):
   User.delete(id)
   flash("Successfuly delete user.", "success")
   return "success"
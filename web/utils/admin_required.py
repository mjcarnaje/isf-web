from functools import wraps

from flask import current_app, flash, redirect
from flask_login import current_user

from ..models import UserRole
from .redirect import get_login_redirect_url


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated:
            if UserRole.check_user_role(current_user.id, "admin"):
                return f(*args, **kwargs)
            else:
                current_app.logger.info(f"Non-admin user {current_user.id} attempted to access admin-required route.")
                flash('You need admin privileges to access this page.', 'warning')
                return redirect(get_login_redirect_url('admin.login', **kwargs))
        else:
            flash('Hold on! To access this feature, you need to log in first.', 'info')
            current_app.logger.info('Redirecting user to the login page.')
            return redirect(get_login_redirect_url('admin.login', **kwargs))

    return wrap
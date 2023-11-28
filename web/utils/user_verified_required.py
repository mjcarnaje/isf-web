from functools import wraps
from flask import redirect, url_for, current_app, flash
from flask_login import current_user
from ..models import UserRole

from  .redirect import get_login_redirect_url

def user_verified_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated:
            if UserRole.check_user_role(current_user.id, "admin"):
                flash('You are an admin! You have no access to this page.', 'info')
                current_app.logger.info('Redirecting admin to the admin index page.')
                return redirect(url_for('admin.index'))
            
            if not current_user.is_verified:
                flash('You need to verify your account first.', 'info')
                current_app.logger.info('Redirecting user to the account verification page.')
                return redirect(url_for('landing.verify_account'))
            
            return f(*args, **kwargs)
        else:
            flash('Hold on! To access this feature, you need to log in first.', 'info')
            current_app.logger.info('Redirecting user to the login page.')
            return redirect(get_login_redirect_url('landing.login', **kwargs))

    return wrap

from functools import wraps

from flask import current_app, flash, redirect, url_for
from flask_login import current_user

from ...models import UserRole
from ..redirect import get_login_redirect_url


def anonymous_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated:
            if UserRole.check_user_role(current_user.id, "admin"):
                return redirect(url_for('admin.index'))
            else:
                return redirect(url_for('user.index'))
        else:
            return f(*args, **kwargs)

    return wrap
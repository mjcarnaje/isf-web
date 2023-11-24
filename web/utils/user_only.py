from functools import wraps

from flask import redirect, url_for
from flask_login import current_user

from ..models import UserRole

def user_only(f):
    @wraps(f)
    def wrap(*args, **kwargs):

        if current_user.is_authenticated:
            if  not UserRole.check_user_role(current_user.id, "admin"):
                return f(*args, **kwargs)
            else:
                return redirect(url_for('admin.index'))
        else:
            return f(*args, **kwargs)

        
    return wrap
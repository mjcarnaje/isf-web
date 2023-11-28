from flask import url_for, request
from flask_login import login_url

def get_login_redirect_url(login_view, **kwargs):
    next_url = url_for(request.endpoint, **kwargs)
        
    login_redirect_url = login_url(login_view=login_view, next_url=next_url)
    return login_redirect_url
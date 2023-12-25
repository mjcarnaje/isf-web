from flask import (Blueprint, render_template)
from flask_login import current_user

from ...utils import user_verified_required
from ...models import Adoption


user_application_bp = Blueprint("application", __name__, url_prefix='/applications')

@user_application_bp.route('', methods=['GET', 'POST'])
@user_verified_required
def applications():
  applications = Adoption.get_applications(current_user.id)
  return render_template('user/applications/applications.html', applications=applications)

@user_application_bp.route('/<int:id>', methods=['GET'])
@user_verified_required
def view_application(id):
  application = Adoption.get_application(id)
  status_history = Adoption.get_application_history(id)
  return render_template('user/applications/application.html', application=application, status_history=status_history)

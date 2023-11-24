from flask import Blueprint, render_template
from ...utils import user_only

volunteer_bp = Blueprint("volunteer", __name__, url_prefix='/volunteer')

@volunteer_bp.route('/', methods=['GET'])
@user_only
def index():
  return render_template('volunteer/volunteer.html')

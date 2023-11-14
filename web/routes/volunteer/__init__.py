from flask import Blueprint, render_template

volunteer_bp = Blueprint("volunteer", __name__, url_prefix='/volunteer')

@volunteer_bp.route('/', methods=['GET'])
def index():
  return render_template('volunteer/volunteer.html')

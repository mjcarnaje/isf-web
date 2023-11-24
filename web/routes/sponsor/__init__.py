from flask import Blueprint, render_template

from ...utils import user_only

sponsor_bp = Blueprint("sponsor", __name__, url_prefix='/sponsor')

@sponsor_bp.route('/', methods=['GET'])
@user_only
def index():
  return render_template('sponsor/sponsor.html')

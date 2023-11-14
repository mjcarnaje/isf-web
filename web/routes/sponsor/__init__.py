from flask import Blueprint, render_template

sponsor_bp = Blueprint("sponsor", __name__, url_prefix='/sponsor')

@sponsor_bp.route('/', methods=['GET'])
def index():
  return render_template('sponsor/sponsor.html')

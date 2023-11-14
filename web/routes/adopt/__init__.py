from flask import Blueprint, render_template

adopt_bp = Blueprint("adopt", __name__, url_prefix='/adopt')

@adopt_bp.route('/', methods=['GET'])
def index():
  return render_template('adopt/adopt.html')

from flask import Blueprint, render_template
from ..utils import user_only

adopt_bp = Blueprint("adopt", __name__, url_prefix='/adopt')

@adopt_bp.route('/', methods=['GET'])
@user_only
def index():
  return render_template('/landing/adopt/adopt.html')

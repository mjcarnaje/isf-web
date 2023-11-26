from flask import Blueprint, render_template
from ...utils import user_only

event_bp = Blueprint("event", __name__, url_prefix='/event')

@event_bp.route('/', methods=['GET'])
@user_only
def index():
  return render_template('event/user_event_list.html')

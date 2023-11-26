from flask import Blueprint, render_template

from ..models import Event
from ..utils import user_only

event_bp = Blueprint("event", __name__, url_prefix='/event')

@event_bp.route('/', methods=['GET'])
@user_only
def index():
  events = Event.find_all(show_landing_page_only=True)
  return render_template('/landing/event/events.html', events=events.get('data'))

@event_bp.route('/<int:id>', methods=['GET'])
@user_only
def view_event(id):
  event = Event.find_by_id(event_id=id)
  return render_template('/landing/event/event.html', event=event)

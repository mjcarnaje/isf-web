from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)
from flask_login import current_user
from ...utils import user_verified_required
from ...models import Event
from ...config import Config

user_event_bp = Blueprint("events", __name__, url_prefix='/events')

@user_event_bp.route('', methods=['GET'])
@user_verified_required
def events():
  events = Event.find_all(page_number=1, page_size=Config.DEFAULT_PAGE_SIZE, filters={})
  return render_template('/user/events/events.html', events=events.get('data'))

@user_event_bp.route('/events/<int:id>', methods=['GET'])
@user_verified_required
def view_event(id):
  event = Event.find_by_id(event_id=id)
  return render_template('/user/events/event.html', event=event)
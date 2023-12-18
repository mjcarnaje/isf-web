from flask import (Blueprint, render_template, request, session)
from flask_login import current_user
from ...utils import user_verified_required, get_active_filter_count, pagination
from ...models import Event, EventPost
from ...config import Config

user_event_bp = Blueprint("events", __name__, url_prefix='/events')

@user_event_bp.route('', methods=['GET'])
@user_verified_required
def events():
    page = request.args.get('page', 1, type=int)
    view_type = session.get('view_type')

    filters = {
        'query': request.args.get('query', '', type=str),
        'who_can_see_it': request.args.get('who_can_see_it', '', type=str),
        'status': request.args.get('status', '', type=str)
    }

    events_query = Event.find_all(
        page_number=page,
        page_size=Config.DEFAULT_PAGE_SIZE,
        filters=filters, 
    )

    events = events_query.get("data")
    total_count = events_query.get("total_count")
    offset = events_query.get("offset")

    return render_template('/user/events/events.html', 
        events=events,
        filters=filters,
        active_filters=get_active_filter_count(filters),
        view_type=view_type,
        pagination = pagination(
            page_number=page,
            offset=offset,
            page_size=Config.DEFAULT_PAGE_SIZE,
            total_count=total_count,
            base_url="user.events.events"
        ),
    )

@user_event_bp.route('/<int:id>', methods=['GET', 'POST'])
@user_verified_required
def view_event(id):
    event = Event.find_by_id(event_id=id)
    status = Event.check_invite_status(event_id=id, user_id=current_user.id)

    if request.method == "POST":
        status = request.form.get("status")
        user_id = current_user.id
        Event.update_status(event_id=id, status=status, user_id=user_id)
        
    
    posts = EventPost.find_posts(event_id=id)

    return render_template('/user/events/event.html', event=event, posts=posts, is_invited=status is not None, status=status)
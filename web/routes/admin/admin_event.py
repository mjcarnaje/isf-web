from flask import Blueprint, redirect, render_template, request, url_for

from ...models import Event
from ...utils import admin_required
from ...validations import AddEventValidation
from flask_login import current_user

admin_event_bp = Blueprint("event", __name__, url_prefix='/event')

@admin_event_bp.route('/', methods=['GET'])
@admin_required
def index():
    events = Event.find_all()
    return render_template('event/admin_event_list.html', events=events.get('data'))

@admin_event_bp.route('/add-event', methods=['GET', 'POST'])
@admin_required
def add_event():
    form = AddEventValidation()
    if form.validate_on_submit():
        new_event = Event(
            name=form.name.data,
            description=form.description.data,
            cover_photo_url=form.cover_photo_url.data,
            start_date=form.start_date.data,
            author_id=current_user.id,
            end_date=form.end_date.data,
            location=form.location.data,
            show_in_landing=form.show_in_landing.data,
            is_done=False    
        )
        Event.insert(new_event)
        return redirect(url_for("admin.event.index"))
    
    return render_template('event/admin_event_add.html', form=form)


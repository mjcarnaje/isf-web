from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user

from ...models import Event
from ...utils import admin_required
from ...validations import AddEventValidation, EditEventValidation

event_bp = Blueprint("event", __name__, url_prefix='/event')

@event_bp.route('/', methods=['GET'])
@admin_required
def events():
    events = Event.find_all()
    return render_template('/admin/event/events.html', events=events.get('data'))

@event_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_event(id):
    event = Event.find_by_id(id)
    form = EditEventValidation()

    if form.validate_on_submit():
        event.name=form.name.data
        event.description=form.description.data
        event.cover_photo_url=form.cover_photo_url.data
        event.start_date=form.start_date.data
        event.end_date=form.end_date.data
        event.location=form.location.data
        event.status=form.status.data
        event.who_can_see_it=form.who_can_see_it.data
        event.volunteer_only=form.volunteer_only.data
        new_pictures = [photo.data for photo in form.pictures.entries if photo.data not in event.pictures]
        event.pictures.extend(new_pictures)        
        Event.edit(event)
        return redirect(url_for("admin.event.events"))
    
    if not form.is_submitted():
        form.id.data = event.id
        form.name.data = event.name
        form.description.data = event.description
        form.cover_photo_url.data = event.cover_photo_url
        form.start_date.data = event.start_date.date()
        form.end_date.data = event.end_date.date()
        form.location.data = event.location
        form.status.data = event.status
        form.who_can_see_it.data = event.who_can_see_it
        form.volunteer_only.data = event.volunteer_only == 1 

        for photo_url in event.pictures:
            form.pictures.append_entry(data=photo_url)
            
    return render_template('/admin/event/edit.html', form=form)

@event_bp.route('/add-event', methods=['GET', 'POST'])
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
            status=form.status.data,
            who_can_see_it=form.who_can_see_it.data,
            volunteer_only=form.volunteer_only.data,            
            pictures=form.pictures.data,
        )
        Event.insert(new_event)
        return redirect(url_for("admin.event.events"))
    
    return render_template('/admin/event/add.html', form=form)

@event_bp.route('/<int:id>/delete', methods=['DELETE'])
@admin_required
def delete_event(id):
    event = Event.find_by_id(id)

    if not event:
        return {"error": "Event not found"}, 404

    Event.delete(id)
    
    return True

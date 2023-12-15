from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)
from flask_login import current_user

from ...config import Config
from ...models import Event, User, Notification
from ...utils import admin_required, get_active_filter_count, pagination
from ...validations import AddEventValidation, EditEventValidation
from ...enums import WhoCanJoinEvent, NotificationType

event_bp = Blueprint("event", __name__, url_prefix='/event')

@event_bp.route('', methods=['GET'])
@admin_required
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

    return render_template('/admin/event/events.html', 
        events=events,
        filters=filters,
        active_filters=get_active_filter_count(filters),
        view_type=view_type,
        pagination = pagination(
            page_number=page,
            offset=offset,
            page_size=Config.DEFAULT_PAGE_SIZE,
            total_count=total_count,
            base_url="admin.event.events"
        ),
    )


@event_bp.route('/<int:id>', methods=['GET'])
@admin_required
def view_event(id):
    event = Event.find_by_id(id)
    statistics = Event.get_statistics(id)

    return render_template('/admin/event/event.html', event=event, statistics=statistics)

@event_bp.route('/<int:id>/members', methods=['GET'])
@admin_required
def event_members(id):
    event = Event.find_by_id(id)
    statistics = Event.get_statistics(id)
    volunteers = Event.get_volunteers(id)

    return render_template('/admin/event/event_members.html', event=event, statistics=statistics, volunteers=volunteers)

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
        event.who_can_see_it=form.who_can_see_it.data
        event.who_can_join=form.who_can_join.data
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
        form.who_can_see_it.data = event.who_can_see_it
        form.who_can_join.data = event.who_can_join

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
            who_can_see_it=form.who_can_see_it.data,
            who_can_join=form.who_can_join.data,            
            pictures=form.pictures.data,
        )
        event_id = Event.insert(new_event)

        if form.who_can_join.data == WhoCanJoinEvent.INVITE_ONLY.value:
            members = User.get_member_users()
            Event.invite_users(event_id=event_id, user_ids=[user['id'] for user in members])

            invite_notifications = []

            for member in members:
                notification = Notification(
                    type=NotificationType.EVENT_INVITED.value,
                    event_id=event_id,
                    user_who_fired_event_id=1,
                    user_to_notify_id=member['id']
                )
                invite_notifications.append(notification)
            Notification.insert_multiple(notifications=invite_notifications)
 
            
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

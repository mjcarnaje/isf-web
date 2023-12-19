from flask import Blueprint, jsonify, render_template, request

from ...config import Config
from ...enums import NotificationType
from ...models import Adoption, Animal, Notification
from ...utils import admin_required, pagination

adoption_bp = Blueprint("adoption", __name__, url_prefix='/adoptions')

@adoption_bp.route('', methods=['GET'])
@admin_required
def adoptions():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query', '', type=str)

    adoption_query = Adoption.get_for_adoptions(
        page_number=page, 
        page_size=Config.DEFAULT_PAGE_SIZE
    )

    animals = adoption_query.get("data")
    total_count = adoption_query.get("total_count")
    offset = adoption_query.get("offset")
    
    return render_template('/admin/adoption/adoptions.html', 
        animals=animals,
        pagination = pagination(
            page_number=page,
            offset=offset,
            page_size=Config.DEFAULT_PAGE_SIZE,
            total_count=total_count,
            base_url="admin.adoption.adoptions"
        ),
    )


@adoption_bp.route('/<int:id>', methods=['GET'])
@admin_required
def adoption(id):
    animal = Animal.find_by_id(id)
    applications = Adoption.get_animal_applications(id)
    return render_template('admin/adoption/adoption.html', animal=animal, applications=applications)

@adoption_bp.route('/<string:animal_id>/interview', methods=['POST'])
@admin_required
def set_interview(animal_id):
    user_id = request.form.get('user_id')
    adoption_id = request.form.get('adoption_id')
    remarks = request.form.get('remarks')
    google_meet_url = request.form.get('google_meet_url')
    zoom_url = request.form.get('zoom_url')

    adoption_status_history_id = Adoption.set_interview(
        adoption_id=adoption_id, 
        remarks=remarks,
        google_meet_url=google_meet_url,
        zoom_url=zoom_url,
    )
    notification = Notification(
        type=NotificationType.ADOPTION_STATUS_UPDATE.value, 
        animal_id=animal_id, 
        adoption_id=adoption_id, 
        adoption_status_history_id=adoption_status_history_id,
        user_who_fired_event_id=1, 
        user_to_notify_id=user_id
    )
    Notification.insert_multiple([notification])

    return jsonify({ 'is_success': True })


@adoption_bp.route('/<string:animal_id>/reject', methods=['POST'])
@admin_required
def set_rejected(animal_id):
    user_id = request.form.get('user_id')
    adoption_id = request.form.get('adoption_id')
    previous_status = request.form.get('previous_status')
    remarks = request.form.get('remarks')
    
    adoption_status_history_id = Adoption.set_rejected(
        adoption_id=adoption_id,
        previous_status=previous_status,
        remarks=remarks
    )
    notification = Notification(
        type=NotificationType.ADOPTION_STATUS_UPDATE.value, 
        animal_id=animal_id, 
        adoption_id=adoption_id, 
        adoption_status_history_id=adoption_status_history_id,
        user_who_fired_event_id=1, 
        user_to_notify_id=user_id
    )    

    Notification.insert_multiple([notification])

    return jsonify({ 'is_success': True })


@adoption_bp.route('/<int:animal_id>/approve', methods=['POST'])
@admin_required
def set_approved(animal_id):
    user_id = request.form.get('user_id')
    adoption_id = request.form.get('adoption_id')
    previous_status = request.form.get('previous_status')
    remarks = request.form.get('remarks')
    
    adoption_status_history_id = Adoption.set_approved(
        adoption_id=adoption_id,
        previous_status=previous_status,
        remarks=remarks
    )
    notification = Notification(
        type=NotificationType.ADOPTION_STATUS_UPDATE.value,
        animal_id=animal_id,
        adoption_id=adoption_id,
        adoption_status_history_id=adoption_status_history_id,
        user_who_fired_event_id=1,
        user_to_notify_id=user_id
    )

    Notification.insert_multiple([notification])


    return jsonify({ 'is_success': True })


@adoption_bp.route('/<int:animal_id>/turnover', methods=['POST'])
@admin_required
def set_turnovered(animal_id):
    user_id = request.form.get('user_id')
    adoption_id = request.form.get('adoption_id')
    previous_status = request.form.get('previous_status')
    remarks = request.form.get('remarks')
    
    adoption_status_history_id = Adoption.set_turnovered(
        adoption_id=adoption_id, 
        animal_id=animal_id, 
        previous_status=previous_status, 
        remarks=remarks
    )
    notification = Notification(
        type=NotificationType.ADOPTION_STATUS_UPDATE.value,
        animal_id=animal_id,
        adoption_id=adoption_id,
        adoption_status_history_id=adoption_status_history_id,
        user_who_fired_event_id=1,
        user_to_notify_id=user_id
    )    
    
    Notification.insert_multiple([notification])

    return jsonify({ 'is_success': True })


from flask import Blueprint, render_template, request, session, jsonify

from ...models import Donation, Notification
from ...utils import admin_required, get_active_filter_count, pagination
from ...config import Config
from ...enums import NotificationType

donations_bp = Blueprint("donations", __name__, url_prefix='/donations')

@donations_bp.route('', methods=['GET'])
@admin_required
def donations():
    page = request.args.get('page', 1, type=int)
    view_type = session.get('view_type')

    filters = {
        'donation_type': request.args.get('donation_type')
    }
    
    donations_query = Donation.find_all(
        page_number=page,
        page_size=Config.DEFAULT_PAGE_SIZE,
        filters=filters
    )

    donations = donations_query.get("data")
    total_count = donations_query.get("total_count")
    offset = donations_query.get("offset")
    
    return render_template('admin/donation/donations.html', 
        donations=donations,
        filters=filters,
        active_filters=get_active_filter_count(filters),
        view_type=view_type,
        pagination = pagination(
            page_number=page,
            offset=offset,
            page_size=Config.DEFAULT_PAGE_SIZE,
            total_count=total_count,
            base_url="admin.donations.donations"
        ),
    )

@donations_bp.route('/<id>', methods=['GET', 'POST'])
def donation(id):
    return render_template('admin/donation/donation.html')


@donations_bp.route('/confirm/<int:id>', methods=['PUT'])
@admin_required
def set_to_confirmed(id):
    Donation.set_to_confirmed(id)
    notification = Notification(
        type=NotificationType.DONATION_STATUS_UPDATE.value,
        donation_id=id,
        user_who_fired_event_id=1,
        user_to_notify_id=request.form.get('user_id')
    )
    notification.insert_multiple([notification])
    return jsonify({ "success": True })

@donations_bp.route('/reject/<int:id>', methods=['PUT'])
@admin_required
def set_to_rejected(id):
    Donation.set_to_rejected(id)
    return jsonify({ "success": True })
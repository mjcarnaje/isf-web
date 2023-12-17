from flask import (Blueprint, render_template, request, session, jsonify, redirect, url_for, flash, current_app)

from ...config import Config
from ...models import AskForHelp, DonationRequestUpdate, DonationRequestDonation
from ...utils import admin_required, get_active_filter_count
from ...utils import pagination, get_image
from ...validations import AddDonationRequestValidation, AddDonationRequestUpdateValidation
from flask_login import current_user

ask_for_help_bp = Blueprint("ask_for_help", __name__, url_prefix='/ask-for-help')

@ask_for_help_bp.route('', methods=['GET'])
@admin_required
def index():
    page = request.args.get('page', 1, type=int)
    view_type = session.get('view_type')

    filters = {
        'query': request.args.get('query', '', type=str),
    }

    donation_requests_query = AskForHelp.find_all(
        page_number=page,
        page_size=Config.DEFAULT_PAGE_SIZE,
        filters=filters
    )

    donation_requests = donation_requests_query.get("data")
    total_count = donation_requests_query.get("total_count")
    offset = donation_requests_query.get("offset")

    return render_template('admin/ask-for-help/donation_requests.html', 
        filters=filters,
        donation_requests=donation_requests,
        active_filters=get_active_filter_count(filters),
        view_type=view_type,
        pagination = pagination(
            page_number=page,
            offset=offset,
            page_size=Config.DEFAULT_PAGE_SIZE,
            total_count=total_count,
            base_url="admin.ask_for_help.index"
        ),
    )

@ask_for_help_bp.route('/<int:id>', methods=['GET', 'POST'])
def view_request(id):
    if request.method == "POST":
        try:
            AskForHelp.set_to_fulfilled(id)
            return jsonify({"status": "success", "message": "Donation request confirmed successfully!"})    
        except Exception as e:
            current_app.logger.error(e)
            return jsonify({"status": "error", "message": "Error confirming donation request. Please try again later."})
    
    return redirect(url_for('admin.ask_for_help.view_request_updates', id=id))
    
@ask_for_help_bp.route('/<int:id>/updates', methods=['GET', 'POST'])
def view_request_updates(id):
    form = AddDonationRequestUpdateValidation()

    if form.validate_on_submit():
        new_update = DonationRequestUpdate(
            donation_request_id=id,
            pictures=form.pictures.data,
            update_text=form.update_text.data,
            user_id=current_user.id
        )
        new_update.insert(new_update)
        return redirect(url_for('admin.ask_for_help.view_request_updates', id=id))
    
    data = AskForHelp.find_one(id)
    posts = DonationRequestUpdate.find_all_by_id(id)
    return render_template('admin/ask-for-help/view_request_updates.html', data=data, posts=posts, form=form)

@ask_for_help_bp.route('/<int:id>/donations', methods=['GET', 'POST'])
def view_request_donations(id):
    data = AskForHelp.find_one(id)
    donations = DonationRequestDonation.find_all_by_id(id)
    return render_template('admin/ask-for-help/view_request_donations.html', data=data, donations=donations)

@ask_for_help_bp.route('/add', methods=['GET', 'POST'])
@admin_required
def add_request():
    form = AddDonationRequestValidation()
    
    if form.validate_on_submit():
        new_donation_request = AskForHelp(
            amount=form.amount.data,
            animal_id=form.animal_id.data,
            description=form.description.data,
            item_list=form.item_list.data,
            pictures=form.pictures.data,
        )
        new_donation_request.insert(new_donation_request)
        return redirect(url_for('admin.ask_for_help.index'))
    
    return render_template('admin/ask-for-help/add_request.html', form=form)


@ask_for_help_bp.route('/<id>/donations/confirm/<donator_id>', methods=['POST'])
@admin_required
def confirm_donation(id, donator_id):
    try:
        DonationRequestDonation.set_to_confirmed(id=donator_id)
        return jsonify({"status": "success", "message": "Donation request confirmed successfully!"})
    except Exception as e:
        current_app.logger.error(e)
        return jsonify({"status": "error", "message": "Error confirming donation request. Please try again later."})

@ask_for_help_bp.route('/<id>/donations/reject/<donator_id>', methods=['POST'])
@admin_required
def reject_donation(id, donator_id):
    try:
        DonationRequestDonation.set_to_rejected(id=donator_id)
        return jsonify({"status": "success", "message": "Donation request rejected successfully!"})
    except Exception as e:
        current_app.logger.error(e)
        return jsonify({"status": "error", "message": "Error rejecting donation request. Please try again later."})


@ask_for_help_bp.route('/animals-options', methods=['GET'])
@admin_required
def get_animal_options():
    animals = AskForHelp.find_animals_options()

    for animal in animals:
        animal['photo_url'] = get_image(animal['photo_url'])

    return jsonify({
        'data': animals
    })
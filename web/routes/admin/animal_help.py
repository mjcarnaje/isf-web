from flask import (Blueprint, render_template, request, session, jsonify, redirect, url_for, flash, current_app)

from ...enums import NotificationType
from ...config import Config
from ...models import AnimalHelp, AnimalHelpPost, Donation, Animal, Notification
from ...utils import admin_required, get_active_filter_count
from ...utils import pagination, upload_images
from ...validations import AddAnimalHelpValidation, AddAnimalHelpPostValidation, EditAnimalHelpValidation
from flask_login import current_user

animal_help_bp = Blueprint("animal_help", __name__, url_prefix='/animal-help')

@animal_help_bp.route('', methods=['GET'])
@admin_required
def index():
    page = request.args.get('page', 1, type=int)
    view_type = session.get('view_type')

    filters = {
        'query': request.args.get('query', '', type=str),
    }

    animal_helps_query = AnimalHelp.find_all(
        page_number=page,
        page_size=Config.DEFAULT_PAGE_SIZE,
        filters=filters
    )

    animal_helps = animal_helps_query.get("data")
    total_count = animal_helps_query.get("total_count")
    offset = animal_helps_query.get("offset")

    return render_template('admin/animal-help/animal_helps.html', 
        filters=filters,
        animal_helps=animal_helps,
        active_filters=get_active_filter_count(filters),
        view_type=view_type,
        pagination = pagination(
            page_number=page,
            offset=offset,
            page_size=Config.DEFAULT_PAGE_SIZE,
            total_count=total_count,
            base_url="admin.animal_help.index"
        ),
    )

@animal_help_bp.route('/<int:id>', methods=['GET', 'POST'])
def view_request(id):
    if request.method == "POST":
        try:
            AnimalHelp.set_to_fulfilled(id)
            flash("Successfuly fulfilled the request!", "success")
            return jsonify({"status": "success", "message": "Donation request confirmed successfully!"})    
        except Exception as e:
            current_app.logger.error(e)
            return jsonify({"status": "error", "message": "Error confirming donation request. Please try again later."})
    
    return redirect(url_for('admin.animal_help.animal_help_posts', id=id))
    
@animal_help_bp.route('/<int:id>/posts', methods=['GET', 'POST'])
def animal_help_posts(id):
    form = AddAnimalHelpPostValidation()

    if request.method == "POST" and form.validate_on_submit():
        new_update = AnimalHelpPost(
            animal_help_id=id,
            pictures=upload_images(form.pictures.data),
            post_text=form.post_text.data,
            user_id=current_user.id
        )
        new_update.insert(new_update)
        flash("Successfully added a post!", "success")
        return redirect(url_for('admin.animal_help.animal_help_posts', id=id))
    
    data = AnimalHelp.find_one(id)
    posts = AnimalHelpPost.find_all_by_id(id)

    return render_template('admin/animal-help/animal_help_posts.html', 
        id=id, 
        data=data, 
        posts=posts, 
        form=form
    )

@animal_help_bp.route('/<int:id>/posts/<int:post_id>', methods=['DELETE'])
def animal_help_post(id, post_id):
    if request.method == "DELETE":
        AnimalHelpPost.delete(post_id=post_id)
        flash("Post deleted!", "success")
        return jsonify({
            'is_success': True
        })
        

@animal_help_bp.route('/<int:id>/donations', methods=['GET', 'POST'])
def animal_help_donations(id):
    data = AnimalHelp.find_one(id)
    donations = Donation.find_all(filters={
        'animal_help_id': id
    }, page_number=1, page_size=100)
    return render_template('admin/animal-help/animal_help_donations.html', data=data, donations=donations)

@animal_help_bp.route('/add', methods=['GET', 'POST'])
@admin_required
def add_animal_help():
    form = AddAnimalHelpValidation()
    
    if form.validate_on_submit():
        new_animal_help = AnimalHelp(
            amount=form.amount.data,
            animal_id=form.animal_id.data,
            description=form.description.data,
            item_list=form.item_list.data,
            thumbnail_url=form.thumbnail_url.data
        )
        new_id = new_animal_help.insert(new_animal_help)
        return redirect(url_for('admin.animal_help.animal_help_posts', id=new_id))
    
    animal = None
    
    if request.args.get("animal_id"):
        form.animal_id.data = request.args.get("animal_id")
        animal = Animal.find_one(request.args.get("animal_id"))

    return render_template('admin/animal-help/add_animal_help.html', form=form, animal=animal)

@animal_help_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_animal_help(id):
    animal_help = AnimalHelp.find_one(id)
    animal = Animal.find_one(animal_help['animal_id'])
    
    form = EditAnimalHelpValidation()
    
    if form.validate_on_submit():
        animal_help = AnimalHelp(
            id=id,
            description=form.description.data,
            amount=form.amount.data,
            item_list=form.item_list.data,
            thumbnail_url=form.thumbnail_url.data
        )
        animal_help.edit(animal_help)
        return redirect(url_for('admin.animal_help.index'))
    
    if not form.is_submitted():
        form.description.data = animal_help['description']
        form.amount.data = animal_help['amount']
        form.item_list.data = animal_help['item_list']
        form.thumbnail_url.data  = animal_help['thumbnail_url']
    
    return render_template('admin/animal-help/edit_animal_help.html', form=form, animal=animal)

@animal_help_bp.route('/<id>/delete', methods=['DELETE'])
@admin_required
def delete_animal_help(id):
    animal_help = AnimalHelp.find_one(id)

    if not animal_help:
        return {"error": "Animal Help not found"}, 404

    AnimalHelp.delete(id)
    
    return {"success": "Successfuly deleted!"}


@animal_help_bp.route('/<id>/donations/confirm/<donation_id>', methods=['POST'])
@admin_required
def confirm_donation(id, donation_id):
    try:
        donation_status_history_id = Donation.set_to_confirmed(id=donation_id)
        notification = Notification(
            type=NotificationType.DONATION_STATUS_UPDATE.value,
            donation_id=donation_id,
            donation_status_history_id=donation_status_history_id,
            user_who_fired_event_id=current_user.id,
            user_to_notify_id=request.form.get('user_id')
        )
        Notification.insert_multiple([notification])
        flash("Donation request confirmed successfully!", "success")
        return jsonify({"status": "success", "message": "Donation request confirmed successfully!"})
    except Exception as e:
        flash("Error confirming donation request. Please try again later.", "error")
        return jsonify({"status": "error", "message": "Error confirming donation request. Please try again later."})

@animal_help_bp.route('/<id>/donations/reject/<donation_id>', methods=['POST'])
@admin_required
def reject_donation(id, donation_id):
    try:
        donation_status_history_id = Donation.set_to_rejected(id=donation_id)
        notification = Notification(
            type=NotificationType.DONATION_STATUS_UPDATE.value,
            donation_id=donation_id,
            donation_status_history_id=donation_status_history_id,
            user_who_fired_event_id=current_user.id,
            user_to_notify_id=request.form.get('user_id')
        )
        Notification.insert_multiple([notification])
        flash("Donation request rejected successfully!", "success")
        return jsonify({"status": "success", "message": "Donation request rejected successfully!"})
    except Exception as e:
        flash("Error rejecting donation request. Please try again later.", "error")
        return jsonify({"status": "error", "message": "Error rejecting donation request. Please try again later."})

@animal_help_bp.route('/<id>/donations/pending/<donation_id>', methods=['POST'])
@admin_required
def pending_donation(id, donation_id):
    try:
        donation_status_history_id = Donation.set_to_pending(id=donation_id)
        notification = Notification(
            type=NotificationType.DONATION_STATUS_UPDATE.value,
            donation_id=donation_id,
            donation_status_history_id=donation_status_history_id,
            user_who_fired_event_id=current_user.id,
            user_to_notify_id=request.form.get('user_id')
        )
        Notification.insert_multiple([notification])
        flash("Donation request set to pending successfully!", "success")
        return jsonify({"status": "success", "message": "Donation request set to  pending successfully!"})
    except Exception as e:
        flash("Error rejecting donation request. Please try again later.", "error")
        return jsonify({"status": "error", "message": "Error rejecting donation request. Please try again later."})


@animal_help_bp.route('/animals-options', methods=['GET'])
@admin_required
def get_animal_options():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query', '', type=str)

    animals = Animal.find_all(page_number=page, page_size=Config.DEFAULT_PAGE_SIZE, filters={
        'query': query,
        'is_adopted': 0,
        'help_requested': 0
    })

    animals_data = animals.get("data")
    total_count = animals.get("total_count")
    offset = animals.get("offset")

    return jsonify({
        'data': animals_data,
        'pagination': pagination(
            page_number=page,
            offset=offset,
            page_size=Config.DEFAULT_PAGE_SIZE,
            total_count=total_count,
            base_url="admin.animal_help.get_animal_options"
        ),
    })
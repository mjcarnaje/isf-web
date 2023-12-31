from flask import Blueprint, flash, redirect, render_template, url_for, request, session
from flask_login import current_user

from ...enums import DonationFor, DonationType, NotificationType
from ...models import Donation, Notification, AnimalHelp, AnimalHelpPost, AnimalHelpDonation
from ...utils import user_verified_required, get_active_filter_count, pagination, upload_images
from ...validations import AddDonation_In_Kind, AddDonationMoney, AddAnimalHelpDonationInKindValidation, AddAnimalHelpDonationMoneyValidation
from ...config import Config

donate_bp = Blueprint("donate", __name__, url_prefix="/donate")

@donate_bp.route('', methods=['GET'])
@user_verified_required
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
  
  return render_template('/user/donate/donate.html',
    filters=filters,
    animal_helps=animal_helps,
    active_filters=get_active_filter_count(filters),
    view_type=view_type,
    pagination = pagination(
        page_number=page,
        offset=offset,
        page_size=Config.DEFAULT_PAGE_SIZE,
        total_count=total_count,
        base_url="user.donate.index"
    ),
  )

@donate_bp.route('/<int:id>', methods=['GET', 'POST'])
def view_request(id):
    return redirect(url_for('user.donate.animal_help_posts', id=id))
  
@donate_bp.route('/<int:id>/updates', methods=['GET', 'POST'])
def animal_help_posts(id):
    data = AnimalHelp.find_one(id)
    posts = AnimalHelpPost.find_all_by_id(id)
    return render_template('user/donate/animal_help_posts.html', data=data, posts=posts)

@donate_bp.route('/<int:id>/donations', methods=['GET', 'POST'])
def animal_help_donations(id):
    data = AnimalHelp.find_one(id)
    donations = AnimalHelpDonation.find_verified_donations(id)
    return render_template('user/donate/animal_help_donations.html', data=data, donations=donations)

@donate_bp.route('/<int:id>/my-donations', methods=['GET', 'POST'])
def animal_help_my_donations(id):
    formid = request.args.get('formid')
    money_form = AddAnimalHelpDonationMoneyValidation()
    in_kind_form = AddAnimalHelpDonationInKindValidation()

    if money_form.validate_on_submit() and formid == 'money':
      new_donation = AnimalHelpDonation(
        amount=money_form.amount.data,
        animal_help_id=id,
        donation_type="Money",
        pictures=upload_images(money_form.pictures.data),
        user_id=current_user.id
      )
      new_donation.insert(new_donation)
      flash("Successfully added a donation", "success")

      return redirect(url_for('user.donate.animal_help_my_donations', id=id))
  
    if in_kind_form.validate_on_submit() and formid == 'in-kind':
      new_donation = AnimalHelpDonation(
        item_list=in_kind_form.item_list.data,
        animal_help_id=id,
        donation_type="In-Kind",
        pictures=upload_images(in_kind_form.pictures.data),
        user_id=current_user.id
      )
      new_donation.insert(new_donation)
      flash("Successfully added a donation", "success")

      return redirect(url_for('user.donate.animal_help_my_donations', id=id))

  
    data = AnimalHelp.find_one(id)
    donations = AnimalHelpDonation.find_donations_by_user_id(animal_help_id=id, user_id=current_user.id)
    
    return render_template('user/donate/animal_help_my_donations.html', money_form=money_form, in_kind_form=in_kind_form, data=data, donations=donations)



@donate_bp.route('/money', methods=['GET', 'POST'])
@user_verified_required
def donate_money():
  form = AddDonationMoney()
    
  if form.validate_on_submit():
    new_donation = Donation(
      remarks=form.remarks.data,
      amount=form.amount.data,
      pictures=upload_images(form.pictures.data),
      donation_type=DonationType.Money.value,
      type=DonationFor.General.value,
      user_id=current_user.id
    )
    donation_id = Donation.insert(new_donation)
    notification = Notification(
      type=NotificationType.ADD_DONATION_MONEY.value,
      donation_id=donation_id,
      user_who_fired_event_id=current_user.id,
      user_to_notify_id=1
    )
    Notification.insert_multiple([notification])

    flash("Successfully added a donation", "success")

    return redirect(url_for('user.donate.index'))
    
  return render_template('/user/donate/donate_money.html', form=form)


@donate_bp.route('/in-kind', methods=['GET', 'POST'])
@user_verified_required
def donate_in_kind():
  form = AddDonation_In_Kind()
    
  if form.validate_on_submit():
    new_donation = Donation(
      remarks=form.remarks.data,
      item_list=form.item_list.data,
      pictures=upload_images(form.pictures.data),
      delivery_type=form.delivery_type.data,
      pick_up_location=form.pick_up_location.data,
      donation_type=DonationType.InKind.value,
      type=DonationFor.General.value,
      user_id=current_user.id
    )
    donation_id = Donation.insert(new_donation)
    notification = Notification(
      type=NotificationType.ADD_DONATION_IN_KIND.value,
      donation_id=donation_id,
      user_who_fired_event_id=current_user.id,
      user_to_notify_id=1
    )
    Notification.insert_multiple([notification])


    flash("Successfully added a donation", "success")
    
    return redirect(url_for('user.donate.index'))
  
  return render_template('/user/donate/donate_in_kind.html', form=form)
   


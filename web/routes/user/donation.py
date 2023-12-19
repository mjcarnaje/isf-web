from flask import Blueprint, flash, redirect, render_template, url_for, request, session
from flask_login import current_user

from ...enums import DonationFor, DonationType, NotificationType
from ...models import Donation, Notification, AskForHelp, DonationRequestUpdate, DonationRequestDonation
from ...utils import user_verified_required, get_active_filter_count, pagination
from ...validations import AddDonation_In_Kind, AddDonationMoney, AddDonationRequestDonationInKindValidation, AddDonationRequestDonationMoneyValidation
from ...config import Config

user_donation_bp = Blueprint("donate", __name__, url_prefix="/donate")

@user_donation_bp.route('', methods=['GET'])
@user_verified_required
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
  
  return render_template('/user/donations/donate.html',
    filters=filters,
    donation_requests=donation_requests,
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

@user_donation_bp.route('/<int:id>', methods=['GET', 'POST'])
def view_request(id):
    return redirect(url_for('user.donate.view_request_updates', id=id))
  
@user_donation_bp.route('/<int:id>/updates', methods=['GET', 'POST'])
def view_request_updates(id):
    data = AskForHelp.find_one(id)
    posts = DonationRequestUpdate.find_all_by_id(id)
    return render_template('user/donations/view_request_updates.html', data=data, posts=posts)

@user_donation_bp.route('/<int:id>/donations', methods=['GET', 'POST'])
def view_request_donations(id):
    formid = request.args.get('formid')
    money_form = AddDonationRequestDonationMoneyValidation()
    in_kind_form = AddDonationRequestDonationInKindValidation()

    if money_form.validate_on_submit() and formid == 'money':
      new_donation = DonationRequestDonation(
        amount=money_form.amount.data,
        donation_request_id=id,
        donation_type="Money",
        pictures=money_form.pictures.data,
        user_id=current_user.id
      )
      new_donation.insert(new_donation)
      flash("Successfully added a donation", "success")
  
    if in_kind_form.validate_on_submit() and formid == 'in-kind':
      new_donation = DonationRequestDonation(
        item_list=in_kind_form.item_list.data,
        donation_request_id=id,
        donation_type="In-Kind",
        pictures=in_kind_form.pictures.data,
        user_id=current_user.id
      )
      new_donation.insert(new_donation)
      flash("Successfully added a donation", "success")
  
    data = AskForHelp.find_one(id)
    donations = DonationRequestDonation.find_all_by_id(id)
    return render_template('user/donations/view_request_donations.html', money_form=money_form, in_kind_form=in_kind_form, data=data, donations=donations)


@user_donation_bp.route('/money', methods=['GET', 'POST'])
@user_verified_required
def donate_money():
  form = AddDonationMoney()
    
  if form.validate_on_submit():
    new_donation = Donation(
      remarks=form.remarks.data,
      amount=form.amount.data,
      pictures=form.pictures.data,
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

    return redirect(url_for('user.donations'))
    
  return render_template('/user/donations/donate_money.html', form=form)


@user_donation_bp.route('/in-kind', methods=['GET', 'POST'])
@user_verified_required
def donate_in_kind():
  form = AddDonation_In_Kind()
    
  if form.validate_on_submit():
    new_donation = Donation(
      remarks=form.remarks.data,
      item_list=form.item_list.data,
      pictures=form.pictures.data,
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
    
    return redirect(url_for('user.donations'))
  
  return render_template('/user/donations/donate_in_kind.html', form=form)
   


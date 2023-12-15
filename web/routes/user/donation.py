from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user

from ...enums import DonationFor, DonationType, NotificationType
from ...models import Donation, Notification
from ...utils import user_verified_required
from ...validations import AddDonation_In_Kind, AddDonationMoney

user_donation_bp = Blueprint("donations", __name__, url_prefix="/donations")

@user_donation_bp.route('/donate', methods=['GET'])
@user_verified_required
def donate():
  return render_template('/user/donations/donate.html')

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
   


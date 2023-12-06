from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, session, url_for)
from flask_login import current_user, login_required, login_user
from werkzeug.security import check_password_hash, generate_password_hash

from ...models import (Donation)
from ...utils import (user_verified_required)
from ...validations import (AddDonation_In_Kind, AddDonationMoney)

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
      donation_type='money',
      type='org',
      user_id=current_user.id
    )
    Donation.insert(new_donation)
    return redirect(url_for('user.dashboard'))

  return render_template('/user/donations/donate_money.html', form=form)


@user_donation_bp.route('/in-kind', methods=['GET', 'POST'])
@user_verified_required
def donate_in_kind():
  form = AddDonation_In_Kind()
    
  if form.validate_on_submit():
    new_donation = Donation(
      remarks=form.remarks.data,
      pictures=form.pictures.data,
      delivery_type=form.delivery_type.data,
      pick_up_location=form.pick_up_location.data,
      donation_type='in_kind',
      type='org',
      user_id=current_user.id
    )
    Donation.insert(new_donation)
    return redirect(url_for('user.dashboard'))
  
  return render_template('/user/donations/donate_in_kind.html', form=form)
   


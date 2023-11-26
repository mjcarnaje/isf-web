from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..models import Donation
from ..utils import user_only
from ..validations import AddDonation_In_Kind, AddDonationMoney

donate_bp = Blueprint("donate", __name__, url_prefix='/donate')

@donate_bp.route('/', methods=['GET'])
@user_only
def index():
  return render_template('/landing/donate/donate.html')


@donate_bp.route('/money', methods=['GET', 'POST'])
@user_only
@login_required
def money():
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

  return render_template('/landing/donate/donate_money.html', form=form)


@donate_bp.route('/in-kind', methods=['GET', 'POST'])
@user_only
@login_required
def in_kind():
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
  
  return render_template('/landing/donate/donate_in_kind.html', form=form)
   
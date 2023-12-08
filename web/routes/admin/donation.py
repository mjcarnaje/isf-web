from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user

from ...models import Donation
from ...utils import admin_required
from ...validations import AddEventValidation

donations_bp = Blueprint("donation", __name__, url_prefix='/donations')

@donations_bp.route('', methods=['GET'])
@admin_required
def donations():
    donations = Donation.get_donations()
    return render_template('admin/donation/donations.html', donations=donations)


@donations_bp.route('/confirm/<int:id>', methods=['POST'])
@admin_required
def set_is_confirmed(id):
    Donation.set_is_confirmed(donation_id=id)
    return redirect(url_for('admin.donation.donations'))

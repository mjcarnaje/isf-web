from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user

from ...models import Donation
from ...utils import admin_required
from ...validations import AddEventValidation

admin_donations_bp = Blueprint("donation", __name__, url_prefix='/donations')

@admin_donations_bp.route('/', methods=['GET'])
@admin_required
def donations():
    donations = Donation.get_donations()
    return render_template('admin/donation/list.html', donations=donations)


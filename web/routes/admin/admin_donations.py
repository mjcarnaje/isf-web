from flask import Blueprint, redirect, render_template, request, url_for

from ...models import Donation
from ...utils import admin_required
from ...validations import AddEventValidation
from flask_login import current_user

admin_donations_bp = Blueprint("donations", __name__, url_prefix='/donations')

@admin_donations_bp.route('/', methods=['GET'])
@admin_required
def index():
    donations = Donation.get_donations()
    return render_template('admin/donations/list.html', donations=donations)


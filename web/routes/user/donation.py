from flask import Blueprint, render_template, request, session

from ...models import Donation
from ...utils import user_verified_required, get_active_filter_count, pagination
from ...config import Config
from flask_login import current_user

user_donation_bp = Blueprint("donation", __name__, url_prefix="/donations")

@user_donation_bp.route('', methods=['GET', 'POST'])
@user_verified_required
def donations():
  page = request.args.get('page', 1, type=int)
  view_type = session.get('view_type')

  filters = {
    'user_id': current_user.id,
    'donation_type': request.args.get('donation_type')
  }
  
  donations_query = Donation.find_all(
      page_number=page,
      page_size=Config.DEFAULT_PAGE_SIZE,
      filters=filters
  )

  donations = donations_query.get("data")
  total_count = donations_query.get("total_count")
  offset = donations_query.get("offset")
    
  return render_template('user/donation/donations.html',
    donations=donations,
    filters=filters,
    active_filters=get_active_filter_count(filters, ["user_id"]),
    view_type=view_type,
    pagination = pagination(
        page_number=page,
        offset=offset,
        page_size=Config.DEFAULT_PAGE_SIZE,
        total_count=total_count,
        base_url="user.donation.donations"
    ),
  )

@user_donation_bp.route('/<id>', methods=['GET', 'POST'])
@user_verified_required
def donation(id):
    return render_template('user/donation/donation.html')


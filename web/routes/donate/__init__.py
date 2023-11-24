from flask import Blueprint, render_template, request
from flask_login import login_required
from ...utils import user_only
from ...validations import AddDonationMoney

donate_bp = Blueprint("donate", __name__, url_prefix='/donate')

@donate_bp.route('/', methods=['GET'])
@user_only
def index():
  return render_template('donate/donate.html')


@donate_bp.route('/money', methods=['GET', 'POST'])
@user_only
@login_required
def money():
  form = AddDonationMoney()
  
  if request.method == 'POST':
    
    if form.validate_on_submit():
      # add to database
      pass
    
  return render_template('donate/donate_money.html', form=form)


@donate_bp.route('/food_materials', methods=['GET', 'POST'])
@user_only
@login_required
def food_materials():
  return render_template('donate/donate_in_kind.html',)
   
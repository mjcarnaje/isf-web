from flask import Blueprint, render_template
from flask_login import login_required
from ...utils import user_only

donate_bp = Blueprint("donate", __name__, url_prefix='/donate')

@donate_bp.route('/', methods=['GET'])
@user_only
def index():
  return render_template('donate/donate.html')


@donate_bp.route('/money', methods=['GET'])
@user_only
@login_required
def money():
    return render_template('donate/donate_money.html')


@donate_bp.route('/food_materials', methods=['GET', 'POST'])
@user_only
@login_required
def food_materials():
    return render_template('donate/donate_in_kind.html',)
   
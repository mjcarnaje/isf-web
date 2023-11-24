from flask import Blueprint, render_template

donate_bp = Blueprint("donate", __name__, url_prefix='/donate')

@donate_bp.route('/', methods=['GET'])
def index():
  return render_template('donate/donate.html')


@donate_bp.route('/money', methods=['GET'])
def money():
    return render_template('donate/donateMoney.html')


@donate_bp.route('/food_materials', methods=['GET', 'POST'])
def food_materials():
 
    return render_template('donate/donateFood_materials.html',)
   
from flask import Blueprint, render_template

donate_bp = Blueprint("donate", __name__, url_prefix='/donate')

@donate_bp.route('/', methods=['GET'])
def index():
  return render_template('donate/donate.html')

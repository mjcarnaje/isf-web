from flask import Blueprint, render_template

from ...utils import user_only
from ...models import Animal

landing_bp = Blueprint("landing", __name__)

@landing_bp.route('/', methods=['GET'])
@user_only
def index():
  animals_query = Animal.find_all(
      page_number=1,
      page_size=6,
  )
  return render_template('home.html', rescue_animals=animals_query.get('data'))
  
@landing_bp.route('/about-us')
def about_us():
    return render_template('about_us.html')

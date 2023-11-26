from flask import Blueprint, render_template

from ..models import Animal
from ..utils import user_only

animal_bp = Blueprint("rescue", __name__, url_prefix='/rescue')

@animal_bp.route('/', methods=['GET'])
@user_only
def index():
  animals = Animal.find_all(page_number=1, page_size=100)
  return render_template('/landing/rescue/rescues.html', animals=animals.get('data'))



from flask import Blueprint, render_template

from ..models import Animal
from ..utils import user_only

animal_bp = Blueprint("rescue", __name__, url_prefix='/rescue')

@animal_bp.route('/', methods=['GET'])
@user_only
def index():
  animals = Animal.find_all(page_number=1, page_size=12)
  return render_template('/landing/rescue/rescues.html', animals=animals.get('data'))

@animal_bp.route('/<int:id>', methods=['GET'])
@user_only
def view_animal(id):
  animal = Animal.find_by_id(id)
  return render_template('/landing/rescue/rescue.html', animal=animal)



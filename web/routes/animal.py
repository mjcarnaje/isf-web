from flask import Blueprint, render_template, request

from ..models import Animal
from ..utils import user_only

animal_bp = Blueprint("rescue", __name__, url_prefix='/rescue')

@animal_bp.route('/', methods=['GET'])
@user_only
def animals():
  page = request.args.get('page', 1, type=int)
  animals_query = Animal.find_all(
              page_number=page, 
              page_size=12
            )
  
  animals = animals_query.get("data")
  has_previous_page = animals_query.get("has_previous_page")
  has_next_page = animals_query.get("has_next_page")
  total_count = animals_query.get("total_count")
  
  return render_template('/landing/rescue/rescues.html',  animals=animals, page_number=page, has_previous_page=has_previous_page, has_next_page=has_next_page, total_count=total_count)

@animal_bp.route('/<int:id>', methods=['GET'])
@user_only
def view_animal(id):
  animal = Animal.find_by_id(id)
  return render_template('/landing/rescue/rescue.html', animal=animal)



from flask import Blueprint, render_template, request

from ..models import Animal
from ..utils import user_only

adopt_bp = Blueprint("adopt", __name__, url_prefix='/adopt')

@adopt_bp.route('/', methods=['GET'])
@user_only
def index():
  page = request.args.get('page', 1, type=int)
  animals_query = Animal.find_all(
              page_number=page, 
              page_size=12,
              filters={
                'for_adoption': True
              }
            )
  
  animals = animals_query.get("data")
  has_previous_page = animals_query.get("has_previous_page")
  has_next_page = animals_query.get("has_next_page")
  total_count = animals_query.get("total_count")
  
  return render_template('/landing/adopt/adopt.html',  animals=animals, page_number=page, has_previous_page=has_previous_page, has_next_page=has_next_page, total_count=total_count)
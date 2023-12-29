from flask import Blueprint, render_template, request, session
from flask_login import current_user

from ...config import Config
from ...models import Animal
from ...utils import (get_active_filter_count, pagination,
                      user_verified_required)

user_animal_bp = Blueprint("animals", __name__, url_prefix='/animals')

@user_animal_bp.route('', methods=['GET'])
@user_verified_required
def animals():
    page = request.args.get('page', 1, type=int)
    view_type = session.get('view_type')

    filters = {
        'query': request.args.get('query', '', type=str),
        'for_adoption': request.args.get('for_adoption') == 'on',
        'is_rescued': request.args.get('is_rescued') == 'on',
        'is_adopted': request.args.get('is_adopted') == 'on',
        'is_dead': request.args.get('is_dead') == 'on',
        'is_dewormed': request.args.get('is_dewormed') == 'on',
        'is_neutered': request.args.get('is_neutered') == 'on',
        'in_shelter': request.args.get('in_shelter') == 'on',
        'gender': request.args.get('gender'),
        'type': request.args.get('type')
    }

    animals_query = Animal.find_all(
        page_number=page,
        page_size=Config.DEFAULT_PAGE_SIZE,
        filters=filters
    )

    animals = animals_query.get("data")
    total_count = animals_query.get("total_count")
    offset = animals_query.get("offset")

    return render_template('user/animals/animals.html', 
        animals=animals,
        filters=filters,
        active_filters=get_active_filter_count(filters),
        view_type=view_type,
        pagination = pagination(
            page_number=page,
            offset=offset,
            page_size=Config.DEFAULT_PAGE_SIZE,
            total_count=total_count,
            base_url="user.animals.animals"
        ),
    )

@user_animal_bp.route('/<int:id>', methods=['GET'])
@user_verified_required
def view_animal(id):
  animal = Animal.find_one(animal_id=id, user_id=current_user.id)
  adopter = Animal.get_adopter(id)
  return render_template('/user/animals/animal.html', animal=animal, adopter=adopter) 
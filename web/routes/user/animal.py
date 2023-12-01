from flask import Blueprint, render_template, request
from ...models import Animal
from ...utils import user_verified_required, get_active_filter_count

user_animal_bp = Blueprint("animal", __name__, url_prefix='/animal')

@user_animal_bp.route('', methods=['GET'])
@user_verified_required
def animals():
    page = request.args.get('page', 1, type=int)
    view_type = request.args.get('view_type', 'table', type=str)

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
        page_size=12,
        filters=filters
    )

    animals = animals_query.get("data")
    has_previous_page = animals_query.get("has_previous_page")
    has_next_page = animals_query.get("has_next_page")
    total_count = animals_query.get("total_count")

    return render_template('user/animal/animals.html', 
                            animals=animals,
                            page_number=page,
                            has_previous_page=has_previous_page,
                            has_next_page=has_next_page,
                            total_count=total_count,
                            filters=filters,
                            active_filters=get_active_filter_count(filters),
                            view_type=view_type
                            )

@user_animal_bp.route('/<int:id>', methods=['GET'])
@user_verified_required
def view_animal(id):
  animal = Animal.find_by_id(id)
  return render_template('/user/animal/animal.html', animal=animal)  
  
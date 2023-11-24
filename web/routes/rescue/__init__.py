from flask import Blueprint, render_template

from ...models import Animal
from ...validations import AnimalValidation
from ...utils import user_only

rescue_bp = Blueprint("rescue", __name__, url_prefix='/rescue')

@rescue_bp.route('/', methods=['GET'])
@user_only
def index():
  return render_template('rescue/rescues.html')



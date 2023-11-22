from flask import Blueprint, render_template

from ...models import Animal
from ...validations import AnimalValidation

rescue_bp = Blueprint("rescue", __name__, url_prefix='/rescue')

@rescue_bp.route('/', methods=['GET'])
def index():
  return render_template('rescue/rescues.html')



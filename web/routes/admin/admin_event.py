from flask import Blueprint, redirect, render_template, request, url_for

from ...models import Animal
from ...utils import admin_required
from ...validations import AnimalValidation
from flask_login import current_user

admin_event_bp = Blueprint("event", __name__, url_prefix='/event')

@admin_event_bp.route('/', methods=['GET'])
@admin_required
def index():
    return render_template('event/admin_event_list.html')

@admin_event_bp.route('/add-event', methods=['GET', 'POST'])
@admin_required
def add_event():
  return render_template('event/admin_event_add.html')


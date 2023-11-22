from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from ...models import Admin
from ...validations import LoginValidation

admin_bp = Blueprint("admin", __name__, url_prefix='/admin')

@admin_bp.route('/', methods=['GET'])
@login_required
def index():
   return render_template('/admin/index.html')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginValidation()

  if form.validate_on_submit():
    admin = Admin.find_by_username(username=form.username.data)

    if admin and check_password_hash(admin.password, form.password.data):
      login_user(admin, remember=True)
      
      next_page = request.args.get("next")

      if next_page:
         return redirect(next_page)
      
      return redirect(url_for('index'))

     
  return render_template('admin/login.html', form=form)


@admin_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


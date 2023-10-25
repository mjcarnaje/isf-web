from flask import Blueprint, render_template, request, redirect, url_for
from ...models import Admin
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

admin_bp = Blueprint("admin", __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():

  if request.method == "POST":
    username = request.form.get('username')
    password = request.form.get('password')

    admin = Admin.find_by_username(username=username)

    if admin and check_password_hash(admin.password, password):
      login_user(admin, remember=True)
      return redirect(url_for('index'))
  
  return render_template('admin/login.html')


@admin_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))
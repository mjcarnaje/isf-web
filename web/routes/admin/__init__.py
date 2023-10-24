from flask import Blueprint, render_template, request

admin_bp = Blueprint("admin", __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():

  if request.method == "POST":
    username = request.form.get('username')
    password = request.form.get('password')
    print(f"Username: {username}, Password: {password}")
  
  return render_template('admin/login.html')
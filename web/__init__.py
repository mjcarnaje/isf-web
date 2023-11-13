from flask import Flask, render_template
from .config import Config
from .database import db
from .database.create_tables import create_tables
from .models import Admin
from flask_login import LoginManager
from werkzeug.security import generate_password_hash


def create_app():    
    app = Flask(__name__)   
    app.config.from_object(Config)

    db.init_app(app)

    create_tables(app)

    # Create default admin user if not exists
    with app.app_context():
        email = app.config['ADMIN_EMAIL']
        username = app.config['ADMIN_USERNAME']
        password = generate_password_hash(app.config['ADMIN_PASSWORD'])
        Admin.insert_ignore(email=email, username=username, password=password)
        
    login_manager = LoginManager()
    login_manager.login_view = 'admin.login'
    login_manager.init_app(app) 

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.find_by_id(user_id=user_id)


    from .routes import admin_bp

    @app.route('/')
    def index():
        return render_template('home.html')
    

    app.register_blueprint(admin_bp)


    return app


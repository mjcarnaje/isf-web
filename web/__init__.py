from flask import Flask, render_template
from .config import Config
from .database import db
from .database.create_tables import create_tables
from .models import Admin
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)   
    
    app.config.from_object(Config)

    db.init_app(app)

    create_tables(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.find_one(user_id=user_id)


    from .routes import auth_bp

    @app.route('/')
    def index():
        return render_template('home.html')
    

    app.register_blueprint(auth_bp)
    
    return app


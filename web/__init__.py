from flask import Flask, render_template, url_for, request, jsonify
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from flask_wtf.csrf import CSRFProtect

from .config import Config
from .database import db
from .database.create_tables import create_tables
from .models import Admin
import cloudinary
from cloudinary.utils import cloudinary_url
from cloudinary.uploader import upload as cloudinary_upload

from .models import Animal

def create_app():    
    app = Flask(__name__)   
    app.config.from_object(Config)

    db.init_app(app)
    CSRFProtect(app)


    create_tables(app)

    # Create default admin user if not exists
    with app.app_context():
        email = app.config['ADMIN_EMAIL']
        username = app.config['ADMIN_USERNAME']
        password = generate_password_hash(app.config['ADMIN_PASSWORD'])
        Admin.insert_ignore(email=email, username=username, password=password)

    cloudinary.config(cloud_name=Config.CLOUDINARY_CLOUD_NAME,
                    api_key=Config.CLOUDINARY_API_KEY,
                    api_secret=Config.CLOUDINARY_API_SECRET,
                    )
        
    login_manager = LoginManager()
    login_manager.login_view = 'admin.login'
    login_manager.init_app(app) 

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.find_by_id(user_id=user_id)

    @app.context_processor
    def utility_processor():
        def get_image(public_id):
            source = public_id if public_id else f"{Config.CLOUDINARY_FOLDER}/default"
            url, options = cloudinary_url(public_id, format="jpg", crop="fill")
            return url
        return dict(get_image=get_image)


    from .routes import (admin_bp, adopt_bp, admin_rescue_bp, donate_bp, rescue_bp, sponsor_bp,
                         volunteer_bp)

    @app.route('/')
    def index():
        animals_query = Animal.find_all(
            page_number=1,
            page_size=6,
        )
        return render_template('home.html', rescue_animals=animals_query.get('data'))
    
    @app.route('/about-us')
    def about_us():
        return render_template('about_us.html')
    
    @app.route('/upload/cloudinary', methods=['POST'])
    def upload_to_cloudinary():
        file = request.files.get('upload')

        if file:
            upload_result = cloudinary_upload(
                file, folder=Config.CLOUDINARY_FOLDER)

            return jsonify({
                'is_success': True,
                'public_id': upload_result['public_id'],
                'url': upload_result['secure_url']
            })

        return jsonify({
            'is_success': False,
            'error': 'Missing file'
        })

        
    app.register_blueprint(admin_bp)
    app.register_blueprint(rescue_bp)
    app.register_blueprint(admin_rescue_bp)
    app.register_blueprint(adopt_bp)
    app.register_blueprint(donate_bp)
    app.register_blueprint(sponsor_bp)
    app.register_blueprint(volunteer_bp)

    return app


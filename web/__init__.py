import cloudinary
from cloudinary.uploader import upload as cloudinary_upload
from flask import Flask, jsonify, request
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from oauthlib.oauth2 import WebApplicationClient

from .commands import set_up_commands
from .config import Config
from .database import db
from .mail import mail
from .models import User
from .socket import socketio
from .utils import celery_init_app, currency, get_image, pretty_date as _pretty_date, sanitize_comma_separated as _sanitize_comma_separated


def  create_app():    
    app = Flask(__name__)

    app.config.from_object(Config)
    db.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)
    
    set_up_commands(app)
    CSRFProtect(app)

    app.config.from_prefixed_env()
    celery_init_app(app)

    cloudinary.config(
        cloud_name=Config.CLOUDINARY_CLOUD_NAME,
        api_key=Config.CLOUDINARY_API_KEY,
        api_secret=Config.CLOUDINARY_API_SECRET,
    )
    
    client = WebApplicationClient(Config.GOOGLE_CLIENT_ID)
        
    login_manager = LoginManager()
    login_manager.login_view = 'landing.login'
    login_manager.init_app(app) 

    @login_manager.user_loader
    def load_user(user_id):
        return User.find_by_id(user_id=user_id)

    @app.context_processor
    def utility_processor():
        return dict(
            get_image=get_image,
        )
    
    @app.template_filter('format_currency')
    def format_currency(n):
        return currency.format_currency(n)

    @app.template_filter('pretty_date')
    def pretty_date(date):
        return _pretty_date(date)

    @app.template_filter('sanitize_comma_separated')
    def sanitize_comma_separated(string):
        return _sanitize_comma_separated(string)
    
    @app.route('/upload/cloudinary', methods=['POST'])
    def upload_to_cloudinary():
        file = request.files.get('upload')

        if not file:
            return jsonify({
                'is_success': False,
                'error': 'Missing file'
            })
        
        size = len(file.read())
        file.seek(0)

        MAX_FILE_SIZE = 1000 * 1000 * 4 # 4mb

        if size > MAX_FILE_SIZE:
            return jsonify({
                'is_success': False,
                'error': 'File too large'
            }), 413

        
        upload_result = cloudinary_upload(
            file, folder=Config.CLOUDINARY_FOLDER)

        return jsonify({
            'is_success': True,
            'public_id': upload_result['public_id'],
            'url': upload_result['secure_url']
        })

    from .routes import admin_bp, landing_bp, user_bp
        
    app.register_blueprint(landing_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)

    return app


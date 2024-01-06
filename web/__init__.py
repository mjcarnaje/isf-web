import logging
import os
from logging.handlers import RotatingFileHandler

import cloudinary
from flask import Flask, send_from_directory
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from .commands import set_up_commands
from .config import Config
from .database import db
from .mail import mail
from .models import User
from .socket import socketio
from .utils import (celery_init_app, format_currency, generate_simple_id,
                    get_image, pretty_date, sanitize_comma_separated,
                    starts_with)


def  create_app():    
    app = Flask(__name__)

    app.logger.setLevel(logging.INFO)
    handler = RotatingFileHandler('app.log', maxBytes=20e6, backupCount=3)
    app.logger.addHandler(handler)

    app.config.from_object(Config)
    db.init_app(app)
    mail.init_app(app)
    socketio.init_app(app, async_mode="eventlet" if Config.FLASK_ENV == "prod" else None, cors_allowed_origins="*")
    
    set_up_commands(app)
    CSRFProtect(app)

    app.config.from_prefixed_env()
    celery_init_app(app)

    cloudinary.config(
        cloud_name=Config.CLOUDINARY_CLOUD_NAME,
        api_key=Config.CLOUDINARY_API_KEY,
        api_secret=Config.CLOUDINARY_API_SECRET,
    )
            
    login_manager = LoginManager()
    login_manager.login_view = 'landing.login'
    login_manager.init_app(app) 

    @login_manager.user_loader
    def load_user(user_id):
        return User.find_one(user_id=user_id)

    @app.context_processor
    def utility_processor():
        return dict(
            get_image=get_image,
            starts_with=starts_with,
            gen_id=generate_simple_id,
        )
    
    app.jinja_env.filters['format_currency'] = format_currency
    app.jinja_env.filters['pretty_date'] = pretty_date
    app.jinja_env.filters['sanitize_comma_separated'] = sanitize_comma_separated
    app.jinja_env.filters['get_image'] = get_image
    
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
    from .routes import admin_bp, common_bp, landing_bp, upload_bp, user_bp

    app.register_blueprint(landing_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(common_bp)

    @app.errorhandler(500)
    def server_error(error):
        app.logger.exception('An exception occurred during a request.')
        return 'Internal Server Error', 500

    return app


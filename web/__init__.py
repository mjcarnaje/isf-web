import cloudinary
from cloudinary.uploader import upload as cloudinary_upload
from cloudinary.utils import cloudinary_url
from flask import Flask, jsonify, flash, request
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from oauthlib.oauth2 import WebApplicationClient

from .config import Config
from .database import db
from .database.run_sql import run_sql
from .mail import mail
from .models import User


def create_app():    
    app = Flask(__name__)

    app.config.from_object(Config)
    db.init_app(app)
    mail.init_app(app)
    
    @app.cli.command("reset")
    def reset_db():
        try:
            app.logger.info("Dropping Database...")
            db.execute_sql(f"DROP DATABASE IF EXISTS {Config.MYSQL_DATABASE};")
            app.logger.info("Database dropped successfully!")
            app.logger.info("---")

            app.logger.info("Creating Database...")
            db.execute_sql(f"CREATE DATABASE {Config.MYSQL_DATABASE};")
            app.logger.info("Database created successfully!")
            app.logger.info("---")

            app.logger.info("Adding tables...")
            run_sql(app, 'create-schema.sql')
            app.logger.info("Tables created successfully!")

            app.logger.info("Seeding data...")
            run_sql(app, 'seed.sql')
            app.logger.info("Seeding completed successfully!")

            app.logger.info("Database reset completed!")
        except Exception as e:
            app.logger.error(f"Error during database reset: {str(e)}")


    CSRFProtect(app)

    cloudinary.config(cloud_name=Config.CLOUDINARY_CLOUD_NAME,
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
        def get_image(public_id):
            source = public_id if public_id else f"{Config.CLOUDINARY_FOLDER}/default"
            url, options = cloudinary_url(source, format="jpg", crop="fill")
            return url
        return dict(get_image=get_image)

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


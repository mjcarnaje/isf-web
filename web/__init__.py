from flask import Flask, render_template, url_for
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
    from .routes import rescue_bp
    from .routes import adopt_bp
    from .routes import donate_bp
    from .routes import sponsor_bp
    from .routes import volunteer_bp

    @app.route('/')
    def index():
        
        # this is temporary, fetch this from db
        rescue_cats = [
            {
                "name": "Fluffy",
                "description": "A playful and affectionate cat.",
                "image_url": url_for('static', filename='images/animal_cat.png')
            },
            {
                "name": "Whiskers",
                "description": "An elegant and curious feline companion.",
                "image_url": url_for('static', filename='images/animal_cat.png')
            },
            {
                "name": "Mittens",
                "description": "A cuddly cat with a love for warm laps.",
                "image_url": url_for('static', filename='images/animal_cat.png')
            },
            {
                "name": "Shadow",
                "description": "A mysterious and independent cat.",
                "image_url": url_for('static', filename='images/animal_cat.png')
            },
            {
                "name": "Sunny",
                "description": "A cheerful and energetic cat with a sunny disposition.",
                "image_url": url_for('static', filename='images/animal_cat.png')
            }
        ]
        
        # this is temporary, fetch this from db
        rescue_dogs = [
            {
                "name": "Buddy",
                "description": "A loyal and friendly canine companion.",
                "image_url": url_for('static', filename='images/animal_dog.png')
            },
            {
                "name": "Max",
                "description": "An energetic and playful dog that loves fetch.",
                "image_url": url_for('static', filename='images/animal_dog.png')
            },
            {
                "name": "Luna",
                "description": "A gentle and loving dog that enjoys long walks.",
                "image_url": url_for('static', filename='images/animal_dog.png')
            },
            {
                "name": "Rocky",
                "description": "A strong and adventurous dog with a love for the outdoors.",
                "image_url": url_for('static', filename='images/animal_dog.png')
            },
            {
                "name": "Coco",
                "description": "A sweet and affectionate dog that adores belly rubs.",
                "image_url": url_for('static', filename='images/animal_dog.png')
            }
        ]

        
        return render_template('home.html', rescue_cats=rescue_cats, rescue_dogs=rescue_dogs)
    
    @app.route('/about-us')
    def about_us():
        return render_template('about_us.html')
    
    app.register_blueprint(admin_bp)
    app.register_blueprint(rescue_bp)
    app.register_blueprint(adopt_bp)
    app.register_blueprint(donate_bp)
    app.register_blueprint(sponsor_bp)
    app.register_blueprint(volunteer_bp)



    return app


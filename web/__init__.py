from flask import Flask, render_template
from config import Config
from database import db


def create_app():
    app = Flask(__name__)   
    
    app.config.from_object(Config)

    db.init_app(app)

    @app.route('/')
    def index():
        return render_template('home.html')
    
    return app


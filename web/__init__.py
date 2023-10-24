from flask import Flask, render_template

app = Flask(__name__)

def create_app():

    @app.route('/')
    def index():
        return render_template('home.html')
    
    return app


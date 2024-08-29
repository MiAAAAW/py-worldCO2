# Flask application setup
from flask import Flask
from os import path

# Launching web app
def create_webapp():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'qwerty asdfgh'

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app

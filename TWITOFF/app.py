# Main twitoff application

# Import important functions
from flask import Flask
from .models import DB
import os


def create_app():
    # create and comfigure a flask app instance
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
        basedir, 'data.sqlite')
    DB.init_app(app)

    @app.route('/')
    def root():
        return 'Welcome to the app!'
    return app

# Main twitoff application

# Import important functions
from flask import Flask


def create_app():
    # create and comfigure a flask app instance
    app = Flask(__name__)

    @app.route('/')
    def root():
        return 'Welcome to the app!'
    return app

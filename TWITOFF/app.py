# Main twitoff application

# Import important functions
from flask import Flask, render_template, request
from .models import DB, User
import os
from decouple import config
from .predict import predict_user
from .twitter import add_or_update_user


def create_app():
    # create and comfigure a flask app instance
    app = Flask(__name__)

    # Find and configure base directory for SQLite
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
        basedir, 'data.sqlite')

    # Turn off SQLAlchemy track modification notifinations
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values['user_name']
        # import pdb; pdb.set_trace()
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = 'User {} successfully added!'.format(name, e)
            tweets = User.query.filter(User.name == name).ones().tweets
        except Exception as e:
            message = 'Error adding {}: {}'.format(name, e)
            tweets = []
        return render_template(
            'user.html', title=name, tweets=tweets, message=message
            )

    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1, user2 = sorted([request.values['user1'],
                               request.values['user2']])
        if user1 == user2:
            message = 'Cannot compare a user to themself!'
        else:
            prediction = predict_user(
                user1, user2, request.values['tweet_text']
                )
            message = '"{}" is more likely to be said by {} than {}'.format(
                request.values['tweet_text'], user1 if prediction else user2,
                user2 if prediction else user1
            )
        return render_template(
            'prediction.html', title='Prediction', message=message
            )

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB Reset', user=[])

    return app

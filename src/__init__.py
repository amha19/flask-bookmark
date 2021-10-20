from flask import Flask
import os
from flask_jwt_extended import JWTManager
from src.bookmark import bookmark
from src.auth import auth
from src.db import db

# from dotenv import load_dotenv

# load_dotenv()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookmark.db'

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.environ['SQLALCHEMY_DB_URI'],

            SQLALCHEMY_TRACK_MODIFICATIONS=False
        )
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    JWTManager(app)
    # db.app = app
    db.init_app(app)
    app.register_blueprint(auth)
    app.register_blueprint(bookmark)

    return app

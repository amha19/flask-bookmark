from flask import Flask, redirect, jsonify
import os
from flask_jwt_extended import JWTManager
import werkzeug
from flask_cors import CORS
from src.bookmark import bookmark
from src.auth import auth
from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from src.db import Bookmark, db

# from dotenv import load_dotenv

# load_dotenv()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    CORS(app)
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

    @app.get('/<short_url>')
    def redirect_to_url(short_url):

        bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()

        if bookmark:
            bookmark.visits += 1
            db.session.commit()

        return redirect(bookmark.url)

    @app.errorhandler(werkzeug.exceptions.NotFound)
    def handle_bad_request(e):
        return jsonify({
            'message': 'Page not found'
        }), HTTP_404_NOT_FOUND

    @app.errorhandler(werkzeug.exceptions.InternalServerError)
    def handle_internal_server_error():
        return 'Something went wrong with the internal server', HTTP_500_INTERNAL_SERVER_ERROR

    return app

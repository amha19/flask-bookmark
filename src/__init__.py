from flask import Flask
import os


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ['SECRET_KEY'],
        )
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    @app.route('/')
    def index():
        return 'Hello, World!'

    @app.route('/hello')
    def say_hello():
        return {'message': 'Hello Flask!'}

    return app

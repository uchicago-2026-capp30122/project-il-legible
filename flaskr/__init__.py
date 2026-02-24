import os

from flask import Flask
from flask_bootstrap import Bootstrap5

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    bootstrap = Bootstrap5(app)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize our data base when creating the app
    from . import db
    db.init_app(app)


    from .blueprints import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')

    # a simple page that says hello
    @app.route('/home')
    def home():
        return 'Hello, World!'

    return app
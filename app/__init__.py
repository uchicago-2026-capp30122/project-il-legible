from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
import logging
from logging.handlers import RotatingFileHandler
import os


bootstrap = Bootstrap5()
db = SQLAlchemy()
migrate = Migrate()


def create_app():

    # Create and configure the app

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # Initialize extensions and database

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)

    # Ensure models are included and associated with the app

    from app import models

    # Tie blueprints to the app

    from .blueprints import home, sponsors, bills, viz, template_filters, api, insights
    from app.cli import bp as cli_bp

    app.register_blueprint(cli_bp)
    app.register_blueprint(home.bp)
    app.register_blueprint(sponsors.bp)
    app.register_blueprint(bills.bp)
    app.register_blueprint(viz.bp)
    app.register_blueprint(insights.bp)
    app.register_blueprint(template_filters.bp)
    app.register_blueprint(api.bp)

    # Logging configuration for production

    if not app.debug and not app.testing:
        # ...

        if app.config["LOG_TO_STDOUT"]:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists("logs"):
                os.mkdir("logs")
            file_handler = RotatingFileHandler(
                "logs/projectillegible.log", maxBytes=10240, backupCount=10
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s: %(message)s "
                    "[in %(pathname)s:%(lineno)d]"
                )
            )
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("Project IL-legible startup")

    return app

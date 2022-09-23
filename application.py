import os
from flask import Blueprint
from app.config import settings
from app.config.restplus import api, application
from app.config.logging import logger
from app.services.ner_service import ns as ner_namespace

api_blueprint = Blueprint('app', __name__, url_prefix='/')


def configure_app(flask_app, config):
    """Define configuration constants."""
    flask_app.config['SERVER_NAME'] = config.FLASK_SERVER_NAME

    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = config.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = config.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = config.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = config.RESTPLUS_ERROR_404_HELP
    flask_app.config['FLASK_DEBUG'] = config.FLASK_DEBUG


def initialize_app(flask_app, api):
    """Configure Flask application."""
    try:
        logger.info("initialisation")
        logger.info(os.environ["RUNNING_ENV"])
        env = getattr(settings, os.environ["RUNNING_ENV"])
    except Exception:
        env = getattr(settings, "Development")
    configure_app(flask_app, env)
    flask_app.api = api
    api.add_namespace(ner_namespace)
    api.init_app(api_blueprint)
    flask_app.register_blueprint(api_blueprint)


# run the app.
if __name__ == "__main__":
    initialize_app(application, api)
    logger.info(">>>>> Starting  server at http://{application.config['SERVER_NAME']}/app/ <<<<<")
    application.run()

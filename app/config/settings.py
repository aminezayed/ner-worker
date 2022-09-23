

# Flask settings
class Config(object):
    FLASK_DEBUG = False
    # Flask-Restplus settings
    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = False
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = True


class Development(Config):
    FLASK_SERVER_NAME = '0.0.0.0:5000'


class Staging(Config):
    FLASK_SERVER_NAME = '0.0.0.0'


class Production(Config):
    FLASK_SERVER_NAME = '0.0.0.0'

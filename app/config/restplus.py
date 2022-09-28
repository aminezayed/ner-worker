from flask_restplus import Api
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix


application = Flask(__name__)
application.wsgi_app = ProxyFix(application.wsgi_app)
api = Api(application, version='1.0', title=' SAM NER wroker',
          description='nlp worker for sam pipeline')

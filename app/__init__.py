from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_httpauth import HTTPTokenAuth
from flask_cors import CORS
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
auth = HTTPTokenAuth(scheme='Bearer')
cors = CORS()
mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app)
    mail.init_app(app)

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app

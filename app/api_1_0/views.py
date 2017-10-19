from . import api
from .. import auth
from flask import g, current_app, jsonify
from flask_login import current_user
from itsdangerous import TimedJSONWebSignatureSerializer as JWT

@api.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % g.current_user

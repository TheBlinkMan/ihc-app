from . import api
from ..models import User, AnonymousUser
from flask import g, jsonify, request, url_for
from flask_login import current_user
from .errors import bad_request, unauthorized, forbidden
from .. import db, auth

@api.route('/users/<int:id>/', methods=['GET'])
@auth.login_required
def get_user(id):
    if g.current_user.id == id:
        return jsonify(g.current_user.to_json()), 200
    # Test if the user is an administrator

    return forbidden('Insufficient credentials')

@api.route('/users/', methods=['POST'])
def create_user():
    user = User.from_json(request.json)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json()), 201, \
        {'Location': url_for('api.get_user', id=user.id, _external=True)}

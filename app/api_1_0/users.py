from . import api
from ..models import User, AnonymousUser
from flask import g, jsonify, request, url_for
from flask_login import current_user
from .errors import bad_request, unauthorized, forbidden
from .. import db, auth
from .decorators import admin_required

@api.route('/users/', methods=['GET'])
@auth.login_required
@admin_required
def get_users():
    return jsonify({'users': [user.to_json() for user in User.query.all()]})

@api.route('/users/<int:id>/', methods=['GET'])
@auth.login_required
def get_user(id):
    if g.current_user.id == id or g.current_user.is_administrator():
        requested_user = User.query.get_or_404(id)
        return jsonify(requested_user.to_json()), 200
    return forbidden('Insufficient credentials')

@api.route('/users/', methods=['POST'])
def create_user():
    user = User.from_json(request.json)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json()), 201, \
        {'Location': url_for('api.get_user', id=user.id, _external=True)}

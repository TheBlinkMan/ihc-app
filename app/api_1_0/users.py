from . import api
from ..models import User, AnonymousUser, Role, get_role_by_email
from flask import g, jsonify, request, url_for
from .errors import bad_request, unauthorized, forbidden
from .. import db, auth
from .decorators import admin_required
from ..email import send_email

@api.route('/users/', methods=['GET'])
@auth.login_required
@admin_required
def get_users():
    return jsonify({'users': [user.to_json() for user in User.query.all()]})

@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    requested_user = User.query.get_or_404(id)
    return jsonify(requested_user.to_json()), 200

@api.route('/users/', methods=['POST'])
def create_user():
    user = User.from_json(request.json)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json()), 201, \
        {'Location': url_for('api.get_user', id=user.id, _external=True)}

@api.route('/users/<int:id>', methods=['PUT'])
@auth.login_required
def update_user(id):

    if g.current_user.id != id and not g.current_user.is_administrator():
        return forbidden('Insufficient credentials')

    user = User.query.get_or_404(id)
    user.lattes = request.json.get('lattes', user.lattes)

    name = request.json.get('name')
    if name is not None:
        if len(name) < 3:
            return bad_request('Invalid name.')
        user.name = name

    password = request.json.get('password')
    if password is not None:
        if len(password) < 8:
            return bad_request('Invalid password.')
        user.password = password

    confirmation_token = request.json.get('confirm')
    if confirmation_token is not None and not user.confirm(confirmation_token):
        return bad_request('Invalid or Expired confirmation token')

    if g.current_user.is_administrator():
        confirm = request.json.get('confirmed', user.confirmed)
        role_id = request.json.get('role_id')
        if role_id is not None:
            role = Role.query.get(role_id)
            if role is None:
                return bad_request('Invalid role.')
            user.role = role

    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json()), 200

@api.route('/confirm', methods = ['GET'])
@auth.login_required
def get_confirmation_token():
    if g.current_user.confirmed:
        return bad_request('User already confirmed his account')
    user = g.current_user
    send_email(user.email, 'Confirm your account', 'email/confirm', user = user, token = user.generate_confirmation_token().decode('ascii'))
    return jsonify({'message': 'A confirmation message was sent to you by email.'}), 200

@api.route('/currentuser', methods=['GET'])
@auth.login_required
def get_current_user():
    return jsonify(g.current_user.to_json()), 200

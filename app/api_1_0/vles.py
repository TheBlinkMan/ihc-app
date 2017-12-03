from . import api
from .decorators import admin_required
from ..models import VirtualLearningEnvironment
from flask import jsonify, current_app, request, g, url_for
from .. import db, auth
from .errors import forbidden
from datetime import datetime

@api.route('/vles/')
def get_vles():
    vles = VirtualLearningEnvironment.query.all()
    return jsonify({"vles": [vle.to_json() for vle in vles]})

@api.route('/vles/<int:id>')
def get_vle(id):
    vle = VirtualLearningEnvironment.query.get_or_404(id)
    return jsonify(vle.to_json()), 200

@api.route('/vles/', methods=['POST'])
@auth.login_required
def create_vle():
    vle = VirtualLearningEnvironment.from_json(request.json)

    vle.author = g.current_user

    db.session.add(vle)
    db.session.commit()

    return jsonify(vle.to_json()), 201, \
            {'Location' : url_for('api.get_vle', id=vle.id, _external=True)}

@api.route('/vles/<int:id>', methods=['PUT'])
@auth.login_required
def update_vle(id):
    vle = VirtualLearningEnvironment.query.get_or_404(id)
    # (TODO) test if the current_user can publish the content
    # and if so change the flag

    if vle.author != g.current_user and not g.current_user.is_administrator():
        return forbidden("Insufficient Permissions")

    vle.name = request.json.get('name', vle.name)
    vle.link = request.json.get('link', vle.link)
    vle.last_modified = datetime.utcnow()

    db.session.add(vle)
    db.session.commit()

    return jsonify(vle.to_json()), 200

@api.route('/vles/<int:id>', methods=['DELETE'])
@auth.login_required
@admin_required
def delete_vle(id):
    vle = VirtualLearningEnvironment.query.get_or_404(id)

    db.session.delete(vle)
    db.session.commit()

    return jsonify({'message': 'The virtual learning environment was deleted.'})

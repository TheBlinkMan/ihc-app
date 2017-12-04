from . import api
from .decorators import admin_required
from ..models import Campus
from flask import jsonify, current_app, request, g, url_for
from .. import db, auth
from .errors import forbidden

@api.route('/campuses/')
def get_campuses():
    return jsonify({"campuses": [campus.to_json() for campus in Campus.query.all()]}), 200

@api.route('/campuses/<int:id>')
def get_campus(id):
    campus = Campus.query.get_or_404(id)
    return jsonify(campus.to_json()), 200

@api.route('/campuses/', methods=['POST'])
@auth.login_required
@admin_required
def create_campus():
    campus = Campus.from_json(request.json)

    db.session.add(campus)
    db.session.commit()

    return jsonify(campus.to_json()), 201, \
            {'Location': url_for('api.get_campus', id=campus.id, _external=True)}

@api.route('/campuses/<int:id>', methods=['PUT'])
@auth.login_required
@admin_required
def update_campus(id):
    campus = Campus.query.get_or_404(id)

    # (TODO) verify for the empty string
    campus.name = request.json.get('name', campus.name)
    campus.localization = request.json.get('localization', campus.localization)

    db.session.add(campus)
    db.session.commit()

    return jsonify(campus.to_json()), 200

@api.route('/campuses/<int:id>', methods=['DELETE'])
@auth.login_required
@admin_required
def delete_campus(id):
    campus = Campus.query.get_or_404(id)

    db.session.delete(campus)
    db.session.commit()

    return jsonify({'message': 'The campus was deleted.'})

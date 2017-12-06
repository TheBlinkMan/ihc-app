from . import api
from .decorators import admin_required
from ..models import Campus, Contact
from flask import jsonify, current_app, request, g, url_for
from .. import db, auth
from .errors import forbidden
from ..validators import is_string_present

@api.route('/contacts/')
def get_contacts():
    return jsonify({"contacts": [contact.to_json() for contact in Contact.query.all()]}), 200

@api.route('/contacts/<int:id>')
def get_contact(id):
    contact = Contact.query.get_or_404(id)
    return jsonify(contact.to_json()), 200

@api.route('/contacts/<int:id>', methods=['PUT'])
@auth.login_required
@admin_required
def update_contact(id):
    contact = Contact.query.get_or_404(id)

    description = request.json.get('description')
    if is_string_present(description):
        contact.description = description

    telephone_number = request.json.get('telephone_number')
    if is_string_present(telephone_number):
        contact.telephone_number = telephone_number

    email = request.json.get('email')
    if is_string_present(email):
        contact.email = email

    # (TODO) update campus?

    db.session.add(contact)
    db.session.commit()

    return jsonify(contact.to_json()), 200

@api.route('/contacts/<int:id>', methods=['DELETE'])
@auth.login_required
@admin_required
def delete_contact(id):
    contact = Contact.query.get_or_404(id)

    db.session.delete(contact)
    db.session.commit()

    return jsonify({'message': 'The contact was deleted.'})

@api.route('/campuses/<int:id>/contacts/', methods=['POST'])
@auth.login_required
@admin_required
def create_campus_contact(id):
    campus = Campus.query.get_or_404(id)

    contact = Contact.from_json(request.json)

    contact.campus = campus

    db.session.add(contact)
    db.session.commit()

    return jsonify(contact.to_json()), 201, \
            {'Location': url_for('api.get_contact', id=campus.id, _external=True)}

@api.route('/campuses/<int:id>/contacts/')
def get_campus_contacts(id):
    campus = Campus.query.get_or_404(id)
    return jsonify({"contacts": [contact.to_json() for contact in campus.contacts]}), 200

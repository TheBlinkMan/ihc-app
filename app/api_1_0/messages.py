from . import api
from .decorators import admin_required
from ..models import Message
from flask import jsonify, current_app, request
from .. import db, auth
from ..email import send_email

@api.route('/messages/<int:id>')
@auth.login_required
@admin_required
def get_message(id):
    message = Message.query.get_or_404(id)
    return jsonify(message.to_json())

@api.route('/messages/', methods=['POST'])
def create_message():
    message = Message.from_json(request.json)

    db.session.add(message)
    db.session.commit()

    send_email(current_app.config['ADMIN_EMAIL'], 'NEW MESSAGE',
            'email/new_message', name = message.name,
            last_name = message.last_name, body = message.body,
            email = message.email)

    return jsonify({'message': 'The message was sent to the course staff.'}), 201

@api.route('/messages/<int:id>', methods=['DELETE'])
@auth.login_required
@admin_required
def delete_message(id):
    message = Message.query.get_or_404(id)

    db.session.delete(message)
    db.session.commit()

    return jsonify({'message': 'The message was deleted.'})

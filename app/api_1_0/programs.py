from . import api
from ..models import Program, Course
from flask import send_from_directory, current_app, g, request, jsonify, url_for
from .authentication import auth
from .errors import bad_request
from ..file_utility import allowed_file, save_file
from .decorators import admin_required
from app import db
import os
from datetime import datetime

@api.route('/programs/')
def get_programs(id):
    program = Program.query.get_or_404(id)
    return jsonify({"programs" :  [url_for('api.get_program', id=program.id, _external=True) for program in Program.query.all()]}), 200

@api.route('/programs/<int:id>')
def get_program(id):
    program = Program.query.get_or_404(id)
    return jsonify(program.to_json())

@api.route('/programs/', methods = ['POST'])
@auth.login_required
@admin_required
def create_program():
    program = Program.from_json(request.json)

    db.session.add(program)
    db.session.commit()

    return jsonify(program.to_json()), 201, \
            {'Location': url_for('api.get_program', id=program.id, _external=True)}

@api.route('/programs/<int:id>', methods = ['PUT'])
@auth.login_required
@admin_required
def update_program(id):
    program = Program.query.get_or_404(id)

    name = request.json.get('name')
    description = request.json.get('description')

    # Validate

    program.name = name
    program.description = description

    db.session.add(program)
    db.session.commit()

    return jsonify(program.to_json())

@api.route('/programs/<int:id>', methods=['DELETE'])
@auth.login_required
@admin_required
def delete_program(id):
    program = Program.query.get_or_404(id)

    db.session.delete(program)
    db.session.commit()

    return jsonify({'message': 'The program was deleted.'})

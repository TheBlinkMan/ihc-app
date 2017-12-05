from . import api
from .decorators import admin_required
from ..models import Program, Course
from flask import jsonify, current_app, request, g, url_for
from .. import db, auth
from .errors import forbidden

@api.route('/courses/')
def get_courses():
    return jsonify({"courses": [course.to_json() for course in Course.query.all()]}), 200

@api.route('/courses/<int:id>')
def get_course(id):
    course = Course.query.get_or_404(id)
    return jsonify(course.to_json()), 200

@api.route('/courses/<int:id>', methods=['PUT'])
@auth.login_required
@admin_required
def update_course(id):
    course = Course.query.get_or_404(id)

    name = request.json.get('name')
    class_hours = request.json.get('class_hours')
    weekly_meetings = request.json.get('weekly_meetings')
    term_load = request.json.get('term_load')
    acronym = request.json.get('acronym')

    #(TODO) VALIDATE

    course.name = name
    course.class_hours = class_hours
    course.weekly_meetings = weekly_meetings
    course.term_load = term_load
    course.acronym = acronym


    db.session.add(course)
    db.session.commit()

    return jsonify(course.to_json()), 200

@api.route('/courses/<int:id>', methods=['DELETE'])
@auth.login_required
@admin_required
def delete_course(id):
    course = Course.query.get_or_404(id)

    db.session.delete(course)
    db.session.commit()

    return jsonify({'message': 'The course was deleted.'})

@api.route('/programs/<int:id>/courses/', methods=['POST'])
@auth.login_required
@admin_required
def create_program_course(id):
    program = Program.query.get_or_404(id)

    course = Course.from_json(request.json)

    course.program = program

    db.session.add(course)
    db.session.commit()

    return jsonify(course.to_json()), 201, \
            {'Location': url_for('api.get_course', id=program.id, _external=True)}

@api.route('/programs/<int:id>/courses/')
def get_program_courses(id):
    program = Program.query.get_or_404(id)
    return jsonify({"courses": [course.to_json() for course in program.courses]}), 200

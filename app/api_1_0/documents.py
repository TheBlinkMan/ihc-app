from . import api
from ..models import Document, Program
from flask import send_from_directory, current_app, g, request, jsonify, url_for
from .authentication import auth
from .errors import bad_request
from ..file_utility import allowed_file, save_file
from .decorators import admin_required
from app import db
import os
from datetime import datetime

@api.route('/documents/<int:id>')
def get_document(id):
    document = Document.query.get_or_404(id)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], document.filename)

@api.route('/documents/<int:id>/metadata/')
def get_document_meta(id):
    document = Document.query.get_or_404(id)
    return jsonify(document.to_json())

@api.route('/documents/', methods = ['POST'])
@auth.login_required
@admin_required
def create_document():
    document = Document.from_json(request.json)

    document.uploaded_by = g.current_user

    db.session.add(document)
    db.session.commit()

    document_string = request.json.get('document_string')
    save_file(os.path.join(current_app.config['UPLOAD_FOLDER'], document.filename), document_string)

    return jsonify(document.to_json()), 201, \
            {'Location': url_for('api.get_document', id=document.id, _external=True)}

@api.route('/documents/<int:id>', methods = ['PUT'])
@auth.login_required
@admin_required
def update_document(id):
    document = Document.query.get_or_404(id)

    filename = request.json.get('filename', document.filename)
    if not allowed_file(filename):
        return bad_request('File must have the extensions: pdf, txt, jpg')
    # check if the filename is already in use and if so generate a random filename
    document.filename = filename

    document.name = request.json.get('name', document.name)
    document_string = request.json.get('document_string')
    save_file(os.path.join(current_app.config['UPLOAD_FOLDER'], document.filename), document_string)

    document.last_modified = datetime.utcnow()

    db.session.add(document)
    db.session.commit()

    return jsonify(document.to_json())

@api.route('/courses/<int:id>/documents/', methods = ['POST'])
@auth.login_required
@admin_required
def create_course_document(id):
    course = Course.query.get_or_404(id)

    document = Document.from_json(request.json)

    document.course = course
    document.uploaded_by = g.current_user

    db.session.add(document)
    db.session.commit()

    return jsonify(document.to_json()), 201, \
            {'Location': url_for('api.get_document', id=document.id, _external=True)}

@api.route('/courses/<int:id>/documents/')
def get_course_documents(id):
    course = Course.query.get_or_404(id)
    return jsonify({"documents" :  [url_for('api.get_document', id=document.id, _external=True) for document in course.documents]}), 200

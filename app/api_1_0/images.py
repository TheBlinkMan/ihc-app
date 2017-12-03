from . import api
from ..models import Image
from flask import send_from_directory, current_app, g, request, jsonify, url_for
from .authentication import auth
from .errors import bad_request
from ..file_utility import allowed_file, save_file
from app import db
import os
from datetime import datetime

@api.route('/images/<int:id>')
def get_image(id):
    image = Image.query.get_or_404(id)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], image.filename)

@api.route('/images/<int:id>/metadata/')
def get_image_meta(id):
    image = Image.query.get_or_404(id)
    return jsonify(image.to_json())

@api.route('/images/', methods = ['POST'])
@auth.login_required
def create_image():
    image = Image.from_json(request.json)
    image.uploaded_by = g.current_user

    db.session.add(image)
    db.session.commit()

    image_string = request.json.get('image_string')
    save_file(os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename), image_string)

    return jsonify(image.to_json()), 201, \
            {'Location': url_for('api.get_image', id=image.id, _external=True)}

@api.route('/images/<int:id>', methods = ['PUT'])
@auth.login_required
def update_image(id):
    image = Image.query.get_or_404(id)

    if image.uploaded_by != g.current_user and not g.current_user.is_administrator():
        return bad_request('Invalid credentials')

    filename = request.json.get('filename')
    if not allowed_file(filename):
        return bad_request('File must have the extensions: pdf, txt, jpg')
    # check if the filename is already in use and if so generate a random filename
    image.filename = filename

    image.alternate = request.json.get('alternate', image.alternate)
    image_string = request.json.get('image_string')
    save_file(os.path.join(current_app.config['UPLOAD_FOLDER'], image.filename), image_string)

    image.last_modified = datetime.utcnow()

    db.session.add(image)
    db.session.commit()

    return jsonify(image.to_json())

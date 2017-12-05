from . import api
from .decorators import admin_required
from ..models import Opportunity, Permission
from flask import jsonify, request, g, url_for
from .. import db, auth

@api.route('/opportunities/')
def get_opportunities():
    return jsonify({"opportunities:" : [opportunity.to_json() for opportunity in Opportunity.query.filter_by(published = True)]})

@api.route('/opportunities/suggested')
def get_suggested_opportunities():
    return jsonify({"opportunities:" : [opportunity.to_json() for opportunity in Opportunity.query.filter_by(published = False)]})

@api.route('/opportunities/<int:id>')
def get_opportunity(id):
    opportunities = Opportunity.query.get_or_404(id)
    return jsonify(opportunities.to_json())

@api.route('/opportunities/', methods=['POST'])
@auth.login_required
def create_opportunity():
    opportunity = Opportunity.from_json(request.json)

    opportunity.author = g.current_user

    if g.current_user.can(Permission.PUBLISH_CONTENT):
        opportunity.published = True

    db.session.add(opportunity)
    db.session.commit()

    return jsonify(opportunity.to_json()), 201, \
            {'Location' : url_for('api.get_opportunity', id=opportunity.id, _external=True)}

@api.route('/opportunities/<int:id>', methods=['PUT'])
@auth.login_required
def update_opportunity(id):
    opportunity = Opportunity.query.get_or_404(id)

    if g.current_user.can(Permission.PUBLISH_CONTENT):
        publish = request.json.get('publish')
        if publish != None:
            if publish in [True, False]:
                opportunity.published =  publish
            else:
                return bad_request('Invalid arguments')

    title = request.json.get('title')

    if title != '' and title != None and len(title) > 3:
        opportunity.title = title

    institution = request.json.get('institution')
    vacancies_amount = request.json.get('vacancies_amount')
    # (TODO) Validation

    opportunity.institution = institution
    opportunity.vacancies_amount = vacancies_amount
    opportunity.description = request.json.get('description', opportunity.description)
    opportunity.link = request.json.get('link', opportunity.link)

    return jsonify(opportunity.to_json()), 200

@api.route('/opportunities/<int:id>', methods=['DELETE'])
@auth.login_required
@admin_required
def delete_opportunity(id):
    opportunity = Opportunity.query.get_or_404(id)

    db.session.delete(opportunity)
    db.session.commit()

    return jsonify({'message': 'The opportunity was deleted.'})

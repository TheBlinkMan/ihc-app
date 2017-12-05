from . import api
from .decorators import admin_required
from ..models import News, Permission
from flask import jsonify, request, g, url_for
from .. import db, auth

@api.route('/news/')
def get_news_items():
    return jsonify({"news:" : [news_item.to_json() for news_item in News.query.filter_by(published = True)]})

@api.route('/news/suggested')
def get_suggested_news_items():
    return jsonify({"news:" : [news_item.to_json() for news_item in News.query.filter_by(published = False)]})

@api.route('/news/<int:id>')
def get_news_item(id):
    news = News.query.get_or_404(id)
    return jsonify(news.to_json())

@api.route('/news/', methods=['POST'])
@auth.login_required
def create_news_item():
    news_item = News.from_json(request.json)

    news_item.author = g.current_user

    if g.current_user.can(Permission.PUBLISH_CONTENT):
        new_item.published = True

    db.session.add(news_item)
    db.session.commit()

    return jsonify(news_item.to_json()), 201, \
            {'Location' : url_for('api.get_news_item', id=news_item.id, _external=True)}

@api.route('/news/<int:id>', methods=['PUT'])
@auth.login_required
def update_news_item(id):
    news_item = News.query.get_or_404(id)

    if g.current_user.can(Permission.PUBLISH_CONTENT):
        publish = request.json.get('publish')
        if publish != None:
            if publish in [True, False]:
                news_item.published =  publish
            else:
                return bad_request('Invalid arguments')

    title = request.json.get('title')

    if title != '' and title != None and len(title) > 3:
        news_item.title = title
    
    news_item.body = request.json.get('body', news_item.body)
    news_item.link = request.json.get('link', news_item.link)

    return jsonify(news_item.to_json()), 200

@api.route('/news/<int:id>', methods=['DELETE'])
@auth.login_required
@admin_required
def delete_news_item(id):
    news_item = News.query.get_or_404(id)

    db.session.delete(news_item)
    db.session.commit()

    return jsonify({'message': 'The news item was deleted.'})

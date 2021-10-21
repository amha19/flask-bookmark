from flask import Blueprint, request, jsonify
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
import validators
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from src.db import Bookmark, db

bookmark = Blueprint("bookmark", __name__, url_prefix="/api/v1/bookmark")


@bookmark.route('/', methods=['POST', 'GET'])
@jwt_required()
def handle_bookmarks():
    current_user = get_jwt_identity()

    if request.method == 'POST':
        body = request.json.get('body', '')
        url = request.json.get('url', '')

        if Bookmark.query.filter_by(url=url).first():
            return jsonify({
                'message': 'url already exist'
            }), HTTP_409_CONFLICT

        if not validators.url(url):
            return jsonify({
                'error': 'Enter valid url'
            }), HTTP_400_BAD_REQUEST

        bookmark = Bookmark(url=url, body=body, user_id=current_user)

        db.session.add(bookmark)
        db.session.commit()

        return jsonify({
            'message': 'Bookmark created',
            'bookmark': {
                'id': bookmark.id,
                'body': bookmark.body,
                'url': bookmark.url,
                'short_url': bookmark.short_url,
                'visits': bookmark.visits,
                'created_at': bookmark.created_at,
                'updated_at': bookmark.updated_at,
            }
        }), HTTP_201_CREATED

    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        bookmarks = Bookmark.query.filter_by(
            user_id=current_user).paginate(page=page, per_page=per_page)

        data = []
        meta = {
            'page': bookmarks.page,
            'pages': bookmarks.pages,
            'totoal_count': bookmarks.total,
            'prev_page': bookmarks.prev_num,
            'next_page': bookmarks.next_num,
            'has_next': bookmarks.has_next,
            'has_prev': bookmarks.has_prev,
        }

        for bookmark in bookmarks.items:
            data.append({
                'body': bookmark.body,
                'url': bookmark.url,
                'short_url': bookmark.short_url,
                'visits': bookmark.visits,
                'created_at': bookmark.created_at,
                'updated_at': bookmark.updated_at,
            })

        return jsonify({
            'bookmarks': data,
            'meta': meta
        }), HTTP_200_OK


@bookmark.get('/<int:bm_id>')
@jwt_required()
def get_bookmark_by_id(bm_id):
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=bm_id).first()

    if not bookmark:
        return jsonify({
            'message': 'Bookmark not found'
        }), HTTP_404_NOT_FOUND

    return jsonify({
        'body': bookmark.body,
        'url': bookmark.url,
        'short_url': bookmark.short_url,
        'visits': bookmark.visits,
        'created_at': bookmark.created_at,
        'updated_at': bookmark.updated_at,
    })

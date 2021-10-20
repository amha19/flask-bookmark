from flask import Blueprint

bookmark = Blueprint("bookmark", __name__, url_prefix="/api/v1/bookmark")


@bookmark.get('/')
def index():
    return {"bookmarks": []}

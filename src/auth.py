from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from src.db import User, db
from src.constants.http_status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT
import validators

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/register')
def register():
    username = request.get_json()['username']
    email = request.get_json()['email']
    password = request.get_json()['password']
    # print(password)

    if not username.isalnum() or " " in username:
        return jsonify({
            "message": "username should be alphanumeric and not contain space"
        }), HTTP_400_BAD_REQUEST

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({
            "message": "Username is already taken"
        }), HTTP_409_CONFLICT

    if len(username) < 4:
        return jsonify({
            "message": "username should have more than 3 characters"
        }), HTTP_400_BAD_REQUEST

    if len(password) < 6:
        return jsonify({
            "message": "Password too short"
        }), HTTP_400_BAD_REQUEST

    pwd_hash = generate_password_hash(password)

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({
            "message": "Email is already taken"
        }), HTTP_409_CONFLICT

    if not validators.email(email):
        return jsonify({
            "message": "Invalid email type"
        })

    user = User(username=username, email=email, password=pwd_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User created",
        "user": {
            "username": username,
            "email": email
        }
    }), HTTP_201_CREATED


@auth.get('/')
def index():
    return {"message": "done"}

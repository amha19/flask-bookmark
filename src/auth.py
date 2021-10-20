from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
import validators
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from werkzeug.security import check_password_hash
from src.db import User, db
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.route('/reg', methods=['POST'])  # alternative way
def to_check():
    username = request.json['username']
    un = request.json.get('username', '')
    return jsonify({'msg': 'ok'}), 200


@auth.post('/register')
def register():
    username = request.get_json()['username']
    email = request.get_json()['email']
    password = request.json['password']

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


@auth.post('/login')
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(email=email).first()

    if user:
        is_pass_corect = check_password_hash(user.password, password)
        if not is_pass_corect:
            return jsonify({
                'message': 'Invalid username or password'
            }), HTTP_401_UNAUTHORIZED
        else:
            access = create_access_token(identity=user.id)
            refresh = create_refresh_token(identity=user.id)

            return jsonify({
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'access_token': access,
                    'refresh_token': refresh
                }
            }), HTTP_200_OK

    return jsonify({
        'error': 'Wrong credentials'
    }), HTTP_401_UNAUTHORIZED


@auth.get('/')
@jwt_required()
def index():
    return {"message": "done"}

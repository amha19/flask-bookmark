from flask import Blueprint

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/register')
def register():
    return "OK", 201


@auth.get('/')
def index():
    return {"message": "done"}

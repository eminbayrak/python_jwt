import jwt
from flask import request, jsonify, Blueprint
from functools import wraps
from werkzeug.security import check_password_hash

auth_blueprint = Blueprint('auth', __name__)

SECRET_KEY = "secret_ape_key"

# Dummy user data for demonstration purposes
users = {
    "user1": {"password": "password1"},
    "user2": {"password": "password2"}
}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['user']
        except Exception as e:
            return jsonify({"message": "Token is invalid!"}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@auth_blueprint.route('/login', methods=['POST'])
def login():
    auth = request.json
    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({"message": "Could not verify"}), 401
    user = users.get(auth.get('username'))
    if not user or not check_password_hash(user['password'], auth.get('password')):
        if user['password'] != auth.get('password'):
            return jsonify({"message": "Could not verify"}), 401
    token = jwt.encode({'user': auth.get('username')}, SECRET_KEY, algorithm="HS256")
    return jsonify({'token': token})

@auth_blueprint.route('/users', methods=['GET'])
@token_required
def get_users(current_user):
    return jsonify({"message": f"Hello {current_user}!"})
from flask import Blueprint, jsonify, request
from app.auth import token_required

user_bp = Blueprint('user', __name__)

@user_bp.route("/", methods=["GET"])
@token_required
def get_users():
    return jsonify({"message": "List of users"})

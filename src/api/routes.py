"""
This module takes care of starting the API Server, loading the DB, and adding the endpoints.
"""

from flask import Flask, request, jsonify, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# Example route
@api.route('/hello', methods=['GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the Google Inspector and you will see the GET request"
    }
    return jsonify(response_body), 200


# SIGNUP route
@api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"msg": "Email and password are required"}), 400

    existing_user = db.session.query(User).filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"msg": "User already exists"}), 400

   
    new_user = User(email=data["email"], password=data["password"], is_active=True)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created"}), 201

#LOGIN route
@api.route('/login', methods = ['POST'])
def login():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"msg": "Email and password are required"}), 400
    
    user = db.session.query(User).filter_by(email = data["email"]).first()
    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"msg": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity=str(user.id))
    return jsonify(access_token=access_token), 200

@api.route('/protected', methods = ['GET'])
@jwt_required()
def protected_route():
    user_id = get_jwt_identity()
    return jsonify({
        "msg": f"Hellow user {user_id}, this is protected content"
    }), 200
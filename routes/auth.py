from datetime import timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Admin, User

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/register_admin", methods=["POST"])
def register_admin():
    data = request.json
    if not data.get("username") or not data.get("password"):
        return jsonify({"message": "Username and password required"}), 400
    hashed_password = generate_password_hash(data["password"])
    new_admin = Admin(username=data["username"], password=hashed_password)
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({"message": "Admin registered successfully"}), 201

@auth_blueprint.route("/register_user", methods=["POST"])
def register_user():
    data = request.json
    if not data.get("username") or not data.get("password"):
        return jsonify({"message": "Username and password required"}), 400
    hashed_password = generate_password_hash(data["password"])
    new_user = User(username=data["username"], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data.get("username") or not data.get("password"):
        return jsonify({"message": "Username and password required"}), 400
    user = Admin.query.filter_by(username=data["username"]).first() or User.query.filter_by(username=data["username"]).first()

    if user and check_password_hash(user.password, data["password"]):
        role = "admin" if isinstance(user, Admin) else "user"
        token = create_access_token(identity={"id": user.id, "role": role}, expires_delta=timedelta(hours=24))
        return jsonify({"access_token": token, "role": role}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

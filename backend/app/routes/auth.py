from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required
from sqlalchemy import func

from ..extensions import db
from ..models import RevokedToken, User
from .helpers import error, require_fields

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    missing = require_fields(data, "username", "email", "password")
    if missing:
        return error(f"Missing required field(s): {', '.join(missing)}")
    if len(data["password"]) < 8:
        return error("Password must be at least 8 characters long.")
    username, email = data["username"].strip(), data["email"].strip().lower()
    existing = User.query.filter((func.lower(User.username) == username.lower()) | (func.lower(User.email) == email)).first()
    if existing:
        return error("A user with that username or email already exists.", 409)
    user = User(username=username, email=email)
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"user": user.to_dict(), "accessToken": create_access_token(identity=str(user.id))}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    missing = require_fields(data, "email", "password")
    if missing:
        return error("Email and password are required.")
    user = User.query.filter(func.lower(User.email) == data["email"].strip().lower()).first()
    if not user or not user.check_password(data["password"]):
        return error("Invalid email or password.", 401)
    return jsonify({"user": user.to_dict(), "accessToken": create_access_token(identity=str(user.id))})


@auth_bp.get("/me")
@jwt_required()
def me():
    user = db.session.get(User, int(get_jwt_identity()))
    if not user:
        return error("User not found.", 404)
    return jsonify({"user": user.to_dict()})


@auth_bp.post("/logout")
@jwt_required()
def logout():
    db.session.add(RevokedToken(jti=get_jwt()["jti"]))
    db.session.commit()
    return "", 204

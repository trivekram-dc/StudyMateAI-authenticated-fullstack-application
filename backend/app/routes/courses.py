from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..extensions import db
from ..models import Course
from .helpers import error

courses_bp = Blueprint("courses", __name__)


def owned_course(course_id, user_id):
    return Course.query.filter_by(id=course_id, user_id=user_id).first()


@courses_bp.get("")
@jwt_required()
def list_courses():
    user_id = int(get_jwt_identity())
    courses = Course.query.filter_by(user_id=user_id).order_by(Course.created_at.desc()).all()
    return jsonify({"courses": [course.to_dict() for course in courses]})


@courses_bp.post("")
@jwt_required()
def create_course():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title:
        return error("Course title is required.")
    course = Course(user_id=int(get_jwt_identity()), title=title, description=str(data.get("description", "")).strip())
    db.session.add(course)
    db.session.commit()
    return jsonify({"course": course.to_dict()}), 201


@courses_bp.get("/<int:course_id>")
@jwt_required()
def get_course(course_id):
    course = owned_course(course_id, int(get_jwt_identity()))
    if not course:
        return error("Course not found.", 404)
    return jsonify({"course": course.to_dict(include_materials=True)})


@courses_bp.put("/<int:course_id>")
@jwt_required()
def update_course(course_id):
    course = owned_course(course_id, int(get_jwt_identity()))
    if not course:
        return error("Course not found.", 404)
    data = request.get_json(silent=True) or {}
    if "title" in data:
        title = str(data["title"]).strip()
        if not title:
            return error("Course title cannot be empty.")
        course.title = title
    if "description" in data:
        course.description = str(data["description"]).strip()
    db.session.commit()
    return jsonify({"course": course.to_dict()})


@courses_bp.delete("/<int:course_id>")
@jwt_required()
def delete_course(course_id):
    course = owned_course(course_id, int(get_jwt_identity()))
    if not course:
        return error("Course not found.", 404)
    db.session.delete(course)
    db.session.commit()
    return "", 204

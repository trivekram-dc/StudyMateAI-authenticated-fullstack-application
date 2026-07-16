from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..extensions import db
from ..models import Course, StudyMaterial
from .helpers import error

materials_bp = Blueprint("materials", __name__)


def owned_material(material_id, user_id):
    return StudyMaterial.query.filter_by(id=material_id, user_id=user_id).first()


@materials_bp.get("")
@jwt_required()
def list_materials():
    user_id = int(get_jwt_identity())
    course_id = request.args.get("courseId", type=int)
    query = StudyMaterial.query.filter_by(user_id=user_id)
    if course_id:
        query = query.filter_by(course_id=course_id)
    materials = query.order_by(StudyMaterial.created_at.desc()).all()
    return jsonify({"materials": [material.to_dict(include_content=False) for material in materials]})


@materials_bp.post("")
@jwt_required()
def create_material():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    title, content = str(data.get("title", "")).strip(), str(data.get("content", "")).strip()
    course_id = data.get("courseId")
    if not title or not content or not course_id:
        return error("Title, course, and study content are required.")
    course = Course.query.filter_by(id=course_id, user_id=user_id).first()
    if not course:
        return error("Course not found.", 404)
    material = StudyMaterial(user_id=user_id, course_id=course.id, title=title, content=content, material_type=str(data.get("materialType", "notes")))
    db.session.add(material)
    db.session.commit()
    return jsonify({"material": material.to_dict()}), 201


@materials_bp.get("/<int:material_id>")
@jwt_required()
def get_material(material_id):
    material = owned_material(material_id, int(get_jwt_identity()))
    if not material:
        return error("Study material not found.", 404)
    return jsonify({"material": material.to_dict()})


@materials_bp.put("/<int:material_id>")
@jwt_required()
def update_material(material_id):
    material = owned_material(material_id, int(get_jwt_identity()))
    if not material:
        return error("Study material not found.", 404)
    data = request.get_json(silent=True) or {}
    for field, column in [("title", "title"), ("content", "content"), ("materialType", "material_type")]:
        if field in data:
            value = str(data[field]).strip()
            if not value:
                return error(f"{field} cannot be empty.")
            setattr(material, column, value)
    db.session.commit()
    return jsonify({"material": material.to_dict()})


@materials_bp.delete("/<int:material_id>")
@jwt_required()
def delete_material(material_id):
    material = owned_material(material_id, int(get_jwt_identity()))
    if not material:
        return error("Study material not found.", 404)
    db.session.delete(material)
    db.session.commit()
    return "", 204

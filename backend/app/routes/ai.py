from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..models import StudyMaterial
from ..services.retrieval import generate_quiz, retrieve, sources_for, summarize
from .helpers import error

ai_bp = Blueprint("ai", __name__)


def material_for_request(data, user_id):
    material_id = data.get("materialId")
    if not material_id:
        return None
    return StudyMaterial.query.filter_by(id=material_id, user_id=user_id).first()


@ai_bp.post("/summarize")
@jwt_required()
def summarize_material():
    material = material_for_request(request.get_json(silent=True) or {}, int(get_jwt_identity()))
    if not material:
        return error("Study material not found.", 404)
    return jsonify({"answer": summarize(material), "sources": sources_for([(1, material, 0, material.content[:700])])})


@ai_bp.post("/ask")
@jwt_required()
def ask_question():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()
    if not question:
        return error("A question is required.")
    material = material_for_request(data, user_id)
    materials = [material] if material else StudyMaterial.query.filter_by(user_id=user_id).all()
    results = retrieve(materials, question)
    if not results:
        return jsonify({"answer": "I couldn't find a relevant passage in your study materials. Try a more specific question or add more notes.", "sources": []})
    excerpts = [chunk for _, _, _, chunk in results]
    answer = "Based on your materials: " + " ".join(excerpts)
    return jsonify({"answer": answer, "sources": sources_for(results)})


@ai_bp.post("/quiz")
@jwt_required()
def quiz_material():
    material = material_for_request(request.get_json(silent=True) or {}, int(get_jwt_identity()))
    if not material:
        return error("Study material not found.", 404)
    return jsonify({"questions": generate_quiz(material), "sources": sources_for([(1, material, 0, material.content[:700])])})

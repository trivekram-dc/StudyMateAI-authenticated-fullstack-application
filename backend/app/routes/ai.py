from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..models import StudyMaterial
from ..services.ai_client import ModelServiceError, generate_grounded_response
from ..services.retrieval import generate_quiz, retrieve, sources_for, summarize
from .helpers import error

ai_bp = Blueprint("ai", __name__)


def material_for_request(data, user_id):
    material_id = data.get("materialId")
    if not material_id:
        return None
    return StudyMaterial.query.filter_by(id=material_id, user_id=user_id).first()


def source_blocks(results):
    return [(index + 1, material.title, chunk) for index, (_, material, _, chunk) in enumerate(results)]


@ai_bp.post("/summarize")
@jwt_required()
def summarize_material():
    material = material_for_request(request.get_json(silent=True) or {}, int(get_jwt_identity()))
    if not material:
        return error("Study material not found.", 404)
    results = [(1, material, 0, material.content[:1400])]
    try:
        answer = generate_grounded_response("Create a short study summary.", "Summarize this material.", source_blocks(results))
    except ModelServiceError as exc:
        return error(str(exc), 503)
    return jsonify({"answer": answer or summarize(material), "sources": sources_for(results), "mode": "model" if answer else "local-fallback"})


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
    try:
        answer = generate_grounded_response("Answer the student's question.", question, source_blocks(results))
    except ModelServiceError as exc:
        return error(str(exc), 503)
    if not answer:
        answer = "Based on your materials: " + " ".join(chunk for _, _, _, chunk in results)
    return jsonify({"answer": answer, "sources": sources_for(results), "mode": "model" if answer else "local-fallback"})


@ai_bp.post("/quiz")
@jwt_required()
def quiz_material():
    material = material_for_request(request.get_json(silent=True) or {}, int(get_jwt_identity()))
    if not material:
        return error("Study material not found.", 404)
    results = [(1, material, 0, material.content[:1400])]
    try:
        answer = generate_grounded_response(
            "Create exactly three concise study questions. Give each answer on the next line.",
            "Turn this material into a self-test quiz.",
            source_blocks(results),
        )
    except ModelServiceError as exc:
        return error(str(exc), 503)
    if answer:
        return jsonify({"answer": answer, "questions": [], "sources": sources_for(results), "mode": "model"})
    return jsonify({"questions": generate_quiz(material), "sources": sources_for(results), "mode": "local-fallback"})

import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .extensions import db


def create_app(test_config=None):
    load_dotenv()
    frontend_dist = Path(__file__).resolve().parent.parent / "frontend_dist"
    app = Flask(__name__, static_folder=str(frontend_dist / "assets"), static_url_path="/assets")
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "development-only-change-me"),
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY", "development-jwt-change-me"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///studymate.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        OPENAI_API_KEY=os.getenv("OPENAI_API_KEY", ""),
        OPENAI_MODEL=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
    )
    if test_config:
        app.config.update(test_config)

    origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    CORS(app, resources={r"/api/*": {"origins": origins}})
    db.init_app(app)
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def is_token_revoked(_jwt_header, jwt_payload):
        from .models import RevokedToken
        return db.session.query(RevokedToken.id).filter_by(jti=jwt_payload["jti"]).first() is not None

    from .routes.ai import ai_bp
    from .routes.auth import auth_bp
    from .routes.courses import courses_bp
    from .routes.materials import materials_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(courses_bp, url_prefix="/api/courses")
    app.register_blueprint(materials_bp, url_prefix="/api/materials")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")

    @app.get("/api/health")
    def health_check():
        return jsonify({"status": "ok"})

    @app.get("/")
    @app.get("/<path:path>")
    def serve_frontend(path=""):
        """Serve the production React build and preserve React Router routes."""
        requested_file = frontend_dist / path
        if path and requested_file.is_file():
            return send_from_directory(frontend_dist, path)
        return send_from_directory(frontend_dist, "index.html")

    with app.app_context():
        db.create_all()
    return app

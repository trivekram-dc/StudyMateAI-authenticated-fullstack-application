from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


def utcnow():
    return datetime.now(timezone.utc)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True, index=True)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)

    courses = db.relationship("Course", back_populates="user", cascade="all, delete-orphan")
    materials = db.relationship("StudyMaterial", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email, "createdAt": self.created_at.isoformat()}


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, default="", nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)

    user = db.relationship("User", back_populates="courses")
    materials = db.relationship("StudyMaterial", back_populates="course", cascade="all, delete-orphan")

    def to_dict(self, include_materials=False):
        data = {"id": self.id, "title": self.title, "description": self.description, "createdAt": self.created_at.isoformat(), "materialCount": len(self.materials)}
        if include_materials:
            data["materials"] = [material.to_dict() for material in self.materials]
        return data


class StudyMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    material_type = db.Column(db.String(40), default="notes", nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)

    user = db.relationship("User", back_populates="materials")
    course = db.relationship("Course", back_populates="materials")

    def to_dict(self, include_content=True):
        data = {"id": self.id, "courseId": self.course_id, "title": self.title, "materialType": self.material_type, "createdAt": self.created_at.isoformat()}
        if include_content:
            data["content"] = self.content
        return data


class RevokedToken(db.Model):
    """Persist revoked JWT IDs so logout invalidates the current access token."""

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(64), nullable=False, unique=True, index=True)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)

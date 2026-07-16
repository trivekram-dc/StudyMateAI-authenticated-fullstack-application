"""Create a safe local demo account and course for reviewers."""

from app import create_app
from app.extensions import db
from app.models import Course, StudyMaterial, User

app = create_app()

with app.app_context():
    if User.query.filter_by(email="demo@studymate.local").first():
        print("Demo account already exists.")
    else:
        user = User(username="demo-student", email="demo@studymate.local")
        user.set_password("DemoPass123!")
        course = Course(title="Introduction to Biology", description="Demo course for reviewing StudyMate.", user=user)
        material = StudyMaterial(
            title="Cell structure notes",
            material_type="notes",
            user=user,
            course=course,
            content=("Cells are the basic units of life. The nucleus stores genetic material. "
                     "The cell membrane controls what enters and leaves a cell. Mitochondria "
                     "release energy from food through cellular respiration."),
        )
        db.session.add_all([user, course, material])
        db.session.commit()
        print("Created demo@studymate.local with password DemoPass123!")

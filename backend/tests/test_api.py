import unittest

from app import create_app
from app.extensions import db


class StudyMateApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://", "JWT_SECRET_KEY": "test-secret"})
        with self.app.app_context():
            db.drop_all(); db.create_all()
        self.client = self.app.test_client()

    def register(self, email="student@example.com", username="student"):
        response = self.client.post("/api/auth/register", json={"email": email, "username": username, "password": "a-secure-password"})
        return response.get_json()["accessToken"]

    def test_course_and_material_are_private(self):
        owner_token = self.register()
        intruder_token = self.register("other@example.com", "other")
        owner_headers = {"Authorization": f"Bearer {owner_token}"}
        intruder_headers = {"Authorization": f"Bearer {intruder_token}"}
        course = self.client.post("/api/courses", headers=owner_headers, json={"title": "Biology"}).get_json()["course"]
        material = self.client.post("/api/materials", headers=owner_headers, json={"courseId": course["id"], "title": "Cell notes", "content": "Cells contain a nucleus and membrane."}).get_json()["material"]
        self.assertEqual(self.client.get(f"/api/courses/{course['id']}", headers=intruder_headers).status_code, 404)
        self.assertEqual(self.client.get(f"/api/materials/{material['id']}", headers=intruder_headers).status_code, 404)

    def test_ask_returns_a_source(self):
        token = self.register(); headers = {"Authorization": f"Bearer {token}"}
        course = self.client.post("/api/courses", headers=headers, json={"title": "Biology"}).get_json()["course"]
        self.client.post("/api/materials", headers=headers, json={"courseId": course["id"], "title": "Cell notes", "content": "The nucleus stores genetic material in a cell."})
        response = self.client.post("/api/ai/ask", headers=headers, json={"question": "What stores genetic material?"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["sources"][0]["materialTitle"], "Cell notes")


if __name__ == "__main__":
    unittest.main()

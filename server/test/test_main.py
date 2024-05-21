import unittest
from fastapi.testclient import TestClient
from ..src.http_server.main import app


class TestMain(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.auth = ('admin', 'password_hash')

    def test_create_student(self):        # Include required fields in the request data
        data = {"name": "Ivan", "date_of_birth": "2000-01-01", "grade": 3, "student_group": "1408"}
        response = self.client.post("/students/", json=data, auth=self.auth)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Student created successfully")

    def test_upload_photo(self):
        photo_content = b"some_test_photo_data"
        response = self.client.post("/students/1/photo", files={"photo": (photo_content, "test.jpg")}, auth=self.auth)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Photo uploaded successfully")

    def test_read_students(self):
        response = self.client.get("/students/", auth=self.auth)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_read_student(self):
        response = self.client.get("/students/1", auth=self.auth)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)

    def test_delete_student(self):
        response = self.client.delete("/students/1", auth=self.auth)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Deleted successfully")


if __name__ == "__main__":
    unittest.main()

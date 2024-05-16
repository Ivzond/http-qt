import unittest
import httpx
from fastapi.testclient import TestClient
from server.src.http_server.main import app


class TestMain(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.auth = ('admin', 'password_hash')  # Use plain password for the test

    def test_create_student(self):
        response = self.client.post("/students/", json={"name": "John Doe"}, auth=self.auth)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Student created successfully")

    def test_upload_photo(self):
        with open("test_photo.jpg", "rb") as photo:
            response = self.client.post("/students/1/photo", files={"photo": photo}, auth=self.auth)
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

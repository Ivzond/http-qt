# test_main.py
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from .main import app


class TestMain(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch('app.crud.create_student')
    def test_create_student(self, mock_create_student):
        mock_create_student.return_value = True
        response = self.client.post("/students/", json={"name": "John", "date_of_birth": "2000-01-01", "grade": 12, "student_group": "A"})
        assert response.status_code == 200
        assert response.json() == "Student created successfully"


if __name__ == '__main__':
    unittest.main()

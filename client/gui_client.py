import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QFileDialog, \
    QMessageBox, QInputDialog
from PyQt5.QtGui import QPixmap
import requests


class FastAPIClient(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create widgets
        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout(self.central_widget)

        # Buttons for each endpoint
        self.create_student_button = QPushButton('Create Student', self)
        self.create_student_button.clicked.connect(self.create_student)

        self.upload_photo_button = QPushButton('Upload Photo', self)
        self.upload_photo_button.clicked.connect(self.upload_photo)

        self.read_students_button = QPushButton('Read Students', self)
        self.read_students_button.clicked.connect(self.read_students)

        self.read_student_button = QPushButton('Read Student', self)
        self.read_student_button.clicked.connect(self.read_student)

        self.delete_student_button = QPushButton('Delete Student', self)
        self.delete_student_button.clicked.connect(self.delete_student)

        # Display area
        self.display_label = QLabel(self)
        self.display_label.setAlignment(Qt.AlignCenter)

        # Add widgets to layout
        self.layout.addWidget(self.create_student_button)
        self.layout.addWidget(self.upload_photo_button)
        self.layout.addWidget(self.read_students_button)
        self.layout.addWidget(self.read_student_button)
        self.layout.addWidget(self.delete_student_button)
        self.layout.addWidget(self.display_label)

        # Set central widget
        self.setCentralWidget(self.central_widget)

        # Set window properties
        self.setWindowTitle('FastAPI Client')
        self.setGeometry(100, 100, 600, 400)

    def create_student(self):
        # Implement logic to create a student using the FastAPI endpoint
        name, ok = QInputDialog.getText(self, 'Enter Student Name', 'Name:')
        if ok:
            date_of_birth, ok = QInputDialog.getText(self, 'Enter Date of Birth', 'Date of Birth (YYYY-MM-DD):')
            if ok:
                grade, ok = QInputDialog.getText(self, 'Enter Grade', 'Grade:')
                if ok:
                    student_group, ok = QInputDialog.getText(self, "Enter Student's group", "Student's Group:")
                    if ok:
                        student_data = {
                            "name": name,
                            "date_of_birth": date_of_birth,
                            "photo": None,
                            "grade": grade,
                            "student_group": student_group
                        }

                        response = requests.post('http://127.0.0.1:8000/students', json=student_data)

                        if response.status_code == 200:
                            QMessageBox.information(self, "Success", "Student successfully created!")
                        else:
                            QMessageBox.warning(self, "Error", f'Failed to create student. Error: {response.text}')

    def upload_photo(self):
        # Implement logic to upload a photo using the FastAPI endpoint
        student_id, ok = QInputDialog.getInt(self, "Enter Student ID", "Student ID:")
        if ok:
            photo_path, _ = QFileDialog.getOpenFileName(self, "Select Photo", "", "Image Files (*.png *.jpg *.bmp)")
            if photo_path:
                with open(photo_path, "rb") as file:
                    photo_bytes = file.read()

                # Example API endpoint for uploading a photo
                response = requests.post(f"http://localhost:8000/students/{student_id}/photo",
                                         files={"photo": photo_bytes})

                if response.status_code == 200:
                    QMessageBox.information(self, "Success", "Photo uploaded successfully.")
                else:
                    QMessageBox.warning(self, "Error", f"Failed to upload photo. Error: {response.text}")

    def read_students(self):
        # Implement logic to read students using the FastAPI endpoint
        pass

    def read_student(self):
        # Implement logic to read a specific student using the FastAPI endpoint
        student_id, ok = QInputDialog.getInt(self, "Enter Student ID", "Student ID:")
        if ok:
            response = requests.get(f'http://127.0.0.1:8000/students/{student_id}')

            if response.status_code == 200:
                student = response.json()
                QMessageBox.information(self, "Student Info", f"Student ID: {student['id']}\nName: {student['name']}")
            else:
                QMessageBox.warning(self, "Error", f"Failed to read student. Error: {response.text}")

    def delete_student(self):
        # Implement logic to delete a student using the FastAPI endpoint
        student_id, ok = QInputDialog.getInt(self, "Enter Student ID", "Student ID:")
        if ok:
            response = requests.delete(f'http://127.0.0.1:8000/students/{student_id}')
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Student successfully deleted!")
            else:
                QMessageBox.warning(self, "Error", f"Failed to delete student. Error: {response.text}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = FastAPIClient()
    client.show()
    sys.exit(app.exec_())

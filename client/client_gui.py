import base64
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, \
    QTextEdit, QFileDialog, QDialog, QFormLayout
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import QUrl, QByteArray, Qt
import sys
import json


class FastAPIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.manager = QNetworkAccessManager()

    def make_request(self, method, endpoint, data=None):
        url = QUrl(self.base_url + endpoint)
        request = QNetworkRequest(url)

        if data:
            request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
            data = json.dumps(data).encode('utf-8')

        reply = self.manager.post(request, data)
        return reply


class CreateStudentForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Create Student Form')

        self.name_label = QLabel('Name:')
        self.name_edit = QLineEdit()

        self.date_of_birth_label = QLabel('Date of Birth (YYYY-MM-DD):')
        self.date_of_birth_edit = QLineEdit()

        self.grade_label = QLabel('Grade:')
        self.grade_edit = QLineEdit()

        self.group_label = QLabel('Student Group:')
        self.group_edit = QLineEdit()

        self.create_button = QPushButton('Create Student')

        layout = QFormLayout()
        layout.addRow(self.name_label, self.name_edit)
        layout.addRow(self.date_of_birth_label, self.date_of_birth_edit)
        layout.addRow(self.grade_label, self.grade_edit)
        layout.addRow(self.group_label, self.group_edit)
        layout.addRow(self.create_button)

        self.setLayout(layout)

        self.create_button.clicked.connect(self.create_student)

    def create_student(self):
        # Get values from the form
        name = self.name_edit.text()
        date_of_birth = self.date_of_birth_edit.text()
        grade = int(self.grade_edit.text())
        group = self.group_edit.text()
        # Call the corresponding method in the main window
        self.parent().create_student(name, date_of_birth, grade, group)
        self.accept()


class UploadPhotoForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Upload photo Form')

        self.id_label = QLabel('ID:')
        self.id_edit = QLineEdit()

        self.photo_label = QLabel('Photo path:')
        self.photo_edit = QLineEdit()

        self.browse_button = QPushButton('Browse')
        self.create_button = QPushButton('Create Student')

        layout = QFormLayout()
        layout.addRow(self.photo_label, self.photo_edit)
        layout.addRow(self.browse_button, self.create_button)

        self.setLayout(layout)

        self.browse_button.clicked.connect(self.browse_photo)
        self.create_button.clicked.connect(self.create_student)

    def browse_photo(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open Photo File', '', 'Image Files (*.png *.jpg *.jpeg)')
        if file_path:
            self.photo_edit.setText(file_path)

    def upload_student(self):
        # Call the corresponding method in the main window
        self.parent().create_student(name, date_of_birth, grade, group)
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self, api_client):
        super().__init__()

        self.api_client = api_client
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Student database')

        # Create widgets
        self.buttons = [
            ("Create Student", "/students/", self.show_create_student_form),
            ("Upload Photo", "/students/{student_id}/photo", self.upload_photo),
            ("Read Students", "/students/", self.read_students),
            ("Read Student", "/students/{student_id}", self.read_student),
            ("Delete Student", "/students/{student_id}", self.delete_student),
        ]

        layout = QVBoxLayout()

        for btn_text, endpoint, slot_function in self.buttons:
            button = QPushButton(btn_text)
            button.clicked.connect(slot_function)
            layout.addWidget(button)

        self.response_text = QTextEdit()
        layout.addWidget(self.response_text)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_create_student_form(self):
        form = CreateStudentForm(self)
        form.exec_()

    def create_student(self, name, date_of_birth, grade, group):
        student_data = {
            "name": name,
            "date_of_birth": date_of_birth,
            "grade": grade,
            "student_group": group,
        }

        reply = self.api_client.make_request("POST", "/students/", student_data)

        self.handle_response(reply)

    def show_upload_photo_form(self):
        form = UploadPhotoForm(self)
        form.exec_()

    def upload_photo(self):
        # Implement the logic for uploading a photo
        pass

    def read_students(self):
        # Implement the logic for reading students
        pass

    def read_student(self):
        pass

    def delete_student(self):
        pass

    def handle_response(self, reply):
        if reply.error():
            self.response_text.setText(f"Error: {reply.errorString()}")
        else:
            response_text = reply.readAll().data().decode('utf-8')
            self.response_text.setText(response_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    api_client = FastAPIClient()
    window = MainWindow(api_client)
    window.show()
    sys.exit(app.exec_())

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QDateEdit,
    QTextEdit,
)
from PyQt5.QtCore import QDate, Qt
from requests import post, get, delete

SERVER_URL = "http://localhost:8000"



class CreateStudentDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.date_of_birth_label = QLabel("Date of Birth:")
        self.date_of_birth_input = QDateEdit()
        self.date_of_birth_input.setCalendarPopup(True)
        self.photo_label = QLabel("Photo:")
        self.photo_button = QPushButton("Choose File")
        self.photo_button.clicked.connect(self.choose_photo)
        self.photo_path = None
        self.grade_label = QLabel("Grade:")
        self.grade_input = QLineEdit()
        self.student_group_label = QLabel("Student Group:")
        self.student_group_input = QLineEdit()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_student)
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.date_of_birth_label)
        self.layout.addWidget(self.date_of_birth_input)
        self.layout.addWidget(self.photo_label)
        self.layout.addWidget(self.photo_button)
        self.layout.addWidget(self.grade_label)
        self.layout.addWidget(self.grade_input)
        self.layout.addWidget(self.student_group_label)
        self.layout.addWidget(self.student_group_input)
        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

    def choose_photo(self):
        self.photo_path, _ = QFileDialog.getOpenFileName(
            self, "Choose photo", "", "Image Files (*.jpg *.png)"
        )

    def save_student(self):
        name = self.name_input.text()
        date_of_birth = self.date_of_birth_input.date().toString(Qt.ISODate)
        if not self.photo_path:
            QMessageBox.warning(self, "Error", "Please select a photo")
            return
        with open(self.photo_path, "rb") as f:
            photo = f.read()
        grade = int(self.grade_input.text())
        student_group = self.student_group_input.text()
        data = {
            "name": name,
            "date_of_birth": date_of_birth,
            "photo": photo,
            "grade": grade,
            "student_group": student_group,
        }
        response = post(f"{SERVER_URL}/students", json=data)
        if response.status_code == 200:
            QMessageBox.information(self, "Success", "Student created successfully")
            self.close()
        else:
            QMessageBox.critical(self, "Error", f"Error creating student: {response.text}")


class ReadStudentDialog(QWidget):
    def __init__(self, student_id):
        super().__init__()
        self.layout = QVBoxLayout()
        self.name_label = QLabel("Name:")
        self.name_value = QLabel("")
        self.date_of_birth_label = QLabel("Date of Birth:")
        self.date_of_birth_value = QLabel("")
        self.photo_label = QLabel("Photo:")
        self.photo_image = QLabel()
        self.photo_image.setScaledContents(True)
        self.grade



from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QDateEdit,
    QTextEdit,
)
from PyQt5.QtCore import QDate, Qt
from requests import post, get, delete

# Replace with your server URL
SERVER_URL = "http://localhost:8000"


class CreateStudentDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.date_of_birth_label = QLabel("Date of Birth:")
        self.date_of_birth_input = QDateEdit()
        self.date_of_birth_input.setCalendarPopup(True)
        self.photo_label = QLabel("Photo:")
        self.photo_button = QPushButton("Choose File")
        self.photo_button.clicked.connect(self.choose_photo)
        self.photo_path = None
        self.grade_label = QLabel("Grade:")
        self.grade_input = QLineEdit()
        self.student_group_label = QLabel("Student Group:")
        self.student_group_input = QLineEdit()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_student)
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.date_of_birth_label)
        self.layout.addWidget(self.date_of_birth_input)
        self.layout.addWidget(self.photo_label)
        self.layout.addWidget(self.photo_button)
        self.layout.addWidget(self.grade_label)
        self.layout.addWidget(self.grade_input)
        self.layout.addWidget(self.student_group_label)
        self.layout.addWidget(self.student_group_input)
        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

    def choose_photo(self):
        self.photo_path, _ = QFileDialog.getOpenFileName(
            self, "Choose Photo", "", "Image Files (*.jpg *.png)"
        )

    def save_student(self):
        name = self.name_input.text()
        date_of_birth = self.date_of_birth_input.date().toString(Qt.ISODate)
        if not self.photo_path:
            QMessageBox.warning(self, "Error", "Please select a photo")
            return
        with open(self.photo_path, "rb") as f:
            photo = f.read()
        grade = int(self.grade_input.text())
        student_group = self.student_group_input.text()
        data = {
            "name": name,
            "date_of_birth": date_of_birth,
            "photo": photo,
            "grade": grade,
            "student_group": student_group,
        }
        response = post(f"{SERVER_URL}/students", json=data)
        if response.status_code == 200:
            QMessageBox.information(self, "Success", "Student created successfully")
            self.close()
        else:
            QMessageBox.critical(self, "Error", f"Error creating student: {response.text}")


class ReadStudentDialog(QWidget):
    def __init__(self, student_id):
        super().__init__()
        self.layout = QVBoxLayout()
        self.name_label = QLabel("Name:")
        self.name_value = QLabel("")
        self.date_of_birth_label = QLabel("Date of Birth:")
        self.date_of_birth_value = QLabel("")
        self.photo_label = QLabel("Photo:")
        self.photo_image = QLabel()
        self.photo_image.setScaledContents(True)
        self.grade = QLabel("Grade:")


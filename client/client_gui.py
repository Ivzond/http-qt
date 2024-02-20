import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from requests import post, get, delete

SERVER_URL = "http://127.0.0.1:8000"


class StudentForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()

        self.date_of_birth_label = QLabel("Date of Birth (YYYY-MM-DD):")
        self.date_of_birth_input = QLineEdit()

        self.grade_label = QLabel("Grade:")
        self.grade_input = QLineEdit()

        self.student_group_label = QLabel("Student group:")
        self.student_group_input = QLineEdit()

        self.create_button = QPushButton("Create Student")
        self.create_button.clicked.connect(self.create_student)

        self.read_button = QPushButton("Read Students")
        self.read_button.clicked.connect(self.read_students)

        self.update_button = QPushButton("Update Student")
        self.update_button.clicked.connect(self.update_student)

        self.delete_button = QPushButton("Delete Student")
        self.delete_button.clicked.connect(self.delete_student)

        layout = QVBoxLayout()
        # layout.addWidget(self.name_label)
        # layout.addWidget(self.name_input)
        # layout.addWidget(self.date_of_birth_label)
        # layout.addWidget(self.date_of_birth_input)
        # layout.addWidget(self.grade_label)
        # layout.addWidget(self.grade_input)
        # layout.addWidget(self.student_group_label)
        # layout.addWidget(self.student_group_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.read_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def create_student(self):
        name = self.name_input.text()
        date_of_birth = self.date_of_birth_input.text()
        grade = int(self.grade_input.text())
        student_group = self.student_group_input.text()

        data = {
            "name": name,
            "date_of_birth": date_of_birth,
            "grade": grade,
            "student_group": student_group,
        }

        response = post(f"{SERVER_URL}/students/", json=data)

        if response.status_code == 200:
            QMessageBox.information(self, "Success", "Student created successfully!")
            self.clear_fields()
        else:
            QMessageBox.critical(self, "Error", f"Error creating student: {response.text}")

    def read_students(self):
        response = get(f"{SERVER_URL}/students/")

        if response.status_code == 200:
            students = response.json()
            text = ""
            for student in students:
                text += f"ID: {student['id']}, Name: {student['name']}\n"
            QMessageBox.information(self, "Students", text)
        else:
            QMessageBox.critical(self, "Error", f"Error reading students: {response.text}")

    def update_student(self):
        pass
        # Implement update functionality here

    def delete_student(self):
        pass
        # Implement delete functionality here

    def clear_fields(self):
        self.name_input.setText("")
        self.date_of_birth_input.setText("")
        self.grade_input.setText("")
        self.student_group_input.setText("")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student database")

        self.form = StudentForm()
        layout = QVBoxLayout()
        layout.addWidget(self.form)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


from PyQt5.QtWidgets import *
import requests
import sys
import base64


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student database")
        self.init_main_menu()

    def init_main_menu(self):
        # Create buttons
        self.read_student_button = QPushButton("Read student", self)
        self.read_students_button = QPushButton("Read students", self)
        self.create_student_button = QPushButton("Create student", self)
        self.upload_photo_button = QPushButton("Upload photo", self)
        self.delete_student_button = QPushButton("Delete student", self)

        # Connect buttons to functions
        self.read_student_button.clicked.connect(self.read_student)
        self.read_students_button.clicked.connect(self.read_students)
        self.create_student_button.clicked.connect(self.create_student)
        self.upload_photo_button.clicked.connect(self.upload_photo)
        self.delete_student_button.clicked.connect(self.delete_student)

        # Arrange buttons vertically
        layout = QVBoxLayout()
        layout.addWidget(self.read_student_button)
        layout.addWidget(self.read_students_button)
        layout.addWidget(self.create_student_button)
        layout.addWidget(self.upload_photo_button)
        layout.addWidget(self.delete_student_button)

        # Set widget layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def read_student(self):
        # Add code to open widget for reading student
        pass

    def read_students(self):
        # Add code to open widget for reading students
        pass

    def create_student(self):
        # Create a separate widget for creating a student
        self.create_widget = QWidget()
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.date_of_birth_input = QLineEdit()
        self.grade_input = QLineEdit()
        self.student_group_input = QLineEdit()
        self.photo_label = QLabel("Photo:")
        self.photo_path_label = QLabel()
        self.photo_button = QPushButton("Choose photo")
        self.photo_button.clicked.connect(self.choose_photo)

        submit_button = QPushButton("Create")
        submit_button.clicked.connect(self.submit_create_student)

        back_button = QPushButton("Back to main menu")
        back_button.clicked.connect(self.init_main_menu)

        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Date of birth (YYYY-MM-DD):"))
        layout.addWidget(self.date_of_birth_input)
        layout.addWidget(QLabel("Grade:"))
        layout.addWidget(self.grade_input)
        layout.addWidget(QLabel("Student group:"))
        layout.addWidget(self.student_group_input)
        layout.addWidget(self.photo_label)
        layout.addWidget(self.photo_path_label)
        layout.addWidget(self.photo_button)
        layout.addWidget(submit_button)
        layout.addWidget(back_button)

        self.create_widget.setLayout(layout)
        self.setCentralWidget(self.create_widget)

    def choose_photo(self):
        # Open file dialog to choose a photo
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg)")
        if file_dialog.exec_():
            self.photo_path = file_dialog.selectedFiles()[0]
            self.photo_path_label.setText(self.photo_path)

    def submit_create_student(self):
        # Get input values
        name = self.name_input.text()
        date_of_birth = self.date_of_birth_input.text()
        grade = self.grade_input.text()
        student_group = self.student_group_input.text()

        payload = {
            "name": name,
            "date_of_birth": date_of_birth,
            "grade": int(grade),
            "student_group": student_group,
        }
        if hasattr(self, 'photo_path') and self.photo_path:
            with open(self.photo_path, 'rb') as file:
                photo_content = file.read()
            # Encode photo content as base64 string
            photo_encoded = base64.b64encode(photo_content).decode('utf-8')
            payload["photo"] = photo_encoded

        # Send request
        url = "http://localhost:8000/students"
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            print("Student created successfully")
        else:
            print("Bad request. Failed to create student")

    def upload_photo(self):
        # Add code to open widget for uploading photo
        pass

    def delete_student(self):
        # Add code to open widget for deleting student
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

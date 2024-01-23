from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QTextEdit, \
    QHBoxLayout
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QUrl, QByteArray


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('FastAPI Client')

        # Create widgets
        self.name_label = QLabel('Name:')
        self.name_edit = QLineEdit()

        self.date_of_birth_label = QLabel('Date of Birth (YYYY-MM-DD):')
        self.date_of_birth_edit = QLineEdit()

        self.grade_label = QLabel('Grade:')
        self.grade_edit = QLineEdit()

        self.group_label = QLabel('Student Group:')
        self.group_edit = QLineEdit()

        self.photo_label = QLabel('Photo path:')
        self.photo_edit = QLineEdit()

        self.send_button = QPushButton('Send Request')
        self.response_text = QTextEdit()

        # Layout
        layout = QVBoxLayout()

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.name_label)
        form_layout.addWidget(self.name_edit)
        form_layout.addWidget(self.date_of_birth_label)
        form_layout.addWidget(self.date_of_birth_edit)
        form_layout.addWidget(self.grade_label)
        form_layout.addWidget(self.grade_edit)
        form_layout.addWidget(self.group_label)
        form_layout.addWidget(self.group_edit)
        form_layout.addWidget(self.photo_label)
        form_layout.addWidget(self.photo_edit)

        layout.addLayout(form_layout)
        layout.addWidget(self.send_button)
        layout.addWidget(self.response_text)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connect button click event to send_request function
        self.send_button.clicked.connect(self.send_request)

    def send_request(self):
        # Get values from the UI
        name = self.name_edit.text()
        date_of_birth = self.date_of_birth_edit.text()
        grade = int(self.grade_edit.text())
        group = self.group_edit.text()
        photo_path = self.photo_edit.text()

        # Read the binary content of the image file
        with open(photo_path, 'rb') as photo_file:
            photo_content = photo_file.read()

        # Make a POST request to the FastAPI server
        self.post_request(name, date_of_birth, grade, group, photo_content)

    def post_request(self, name, date_of_birth, grade, group, photo_content):
        url = QUrl("http://localhost:8000/students/")

        # Create QNetworkRequest
        request = QNetworkRequest(url)
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")

        # Create QNetworkAccessManager
        manager = QNetworkAccessManager()

        # Convert payload to bytes
        data = QByteArray()

        # Append JSON payload
        data.append(
            f'{{"name":"{name}", "date_of_birth":"{date_of_birth}", "grade":{grade}, "student_group":"{group}", "photo": null}}')

        # Append binary photo content
        data.append(photo_content)

        # Send POST request
        reply = manager.post(request, data)

        # Connect signals for handling the response
        reply.finished.connect(self.handle_response)

    def handle_response(self):
        reply = self.sender()

        if reply.error():
            self.response_text.setText(f"Error: {reply.errorString()}")
        else:
            response_text = reply.readAll().data().decode('utf-8')
            self.response_text.setText(response_text)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

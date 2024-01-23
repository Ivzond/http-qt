import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QLineEdit, QWidget
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


class MyClientApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

        # Create QNetworkAccessManager
        self.network_manager = QNetworkAccessManager(self)

    def init_ui(self):
        self.setWindowTitle("FastAPI Client")
        self.setGeometry(100, 100, 600, 400)

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Create widgets (buttons, text boxes, etc.) as needed

        # Example button
        self.btn_send_request = QPushButton("Send Request", self)
        self.btn_send_request.clicked.connect(self.send_request)
        layout.addWidget(self.btn_send_request)

        # Example label
        self.lbl_response = QLabel("Response will be displayed here", self)
        layout.addWidget(self.lbl_response)

    def send_request(self):
        # Example request to get all students
        request = QNetworkRequest(QUrl("http://localhost:8000/students/"))
        reply = self.network_manager.get(request)

        # Connect signals to handle the response
        reply.finished.connect(self.handle_request_finished)

    def handle_request_finished(self):
        reply = self.sender()
        if reply.error() == QNetworkReply.NoError:
            # Handle successful response
            data = reply.readAll()
            self.lbl_response.setText(f'Response: {data.decode()}')
        else:
            # Handle error
            self.lbl_response.setText(f'Error: {reply.errorString()}')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client_app = MyClientApp()
    client_app.show()
    sys.exit(app.exec_())

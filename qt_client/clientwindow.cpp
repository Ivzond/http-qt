#include "clientwindow.h"
#include <QVBoxLayout>
#include <QFormLayout>
#include <QJsonObject>
#include <QHttpMultiPart>

ClientWindow::ClientWindow(QWidget *parent) : QWidget(parent) {
    createStudentButton = new QPushButton("Create Student", this);
    uploadPhotoButton = new QPushButton("Upload Photo", this);
    readStudentsButton = new QPushButton("Read Students", this);
    readStudentButton = new QPushButton("Read Student", this);
    deleteStudentButton = new QPushButton("Delete Student", this);

    connect(createStudentButton, &QPushButton::clicked, this, &ClientWindow::openCreateStudentWindow);
    connect(uploadPhotoButton, &QPushButton::clicked, this, &ClientWindow::openUploadPhotoWindow);
    connect(readStudentsButton, &QPushButton::clicked, this, &ClientWindow::readStudentsRequest);
    connect(readStudentButton, &QPushButton::clicked, this, &ClientWindow::openReadStudentWindow);
    connect(deleteStudentButton, &QPushButton::clicked, this, &ClientWindow::openDeleteStudentWindow);

    QVBoxLayout *layout = new QVBoxLayout(this);
    layout->addWidget(createStudentButton);
    layout->addWidget(uploadPhotoButton);
    layout->addWidget(readStudentsButton);
    layout->addWidget(readStudentButton);
    layout->addWidget(deleteStudentButton);

    setLayout(layout);

    networkManager = new QNetworkAccessManager(this);
}

void ClientWindow::openCreateStudentWindow() {
    QDialog *dialog = new QDialog(this);
    QFormLayout *formLayout = new QFormLayout(dialog);

    createStudentNameLineEdit = new QLineEdit(dialog);
    createStudentNameLineEdit->setPlaceholderText("Иванов И.И.");
    createStudentDOBLineEdit = new QLineEdit(dialog);
    createStudentDOBLineEdit->setPlaceholderText("ГГГГ-ММ-ДД");
    createStudentGradeLineEdit = new QLineEdit(dialog);
    createStudentGradeLineEdit->setPlaceholderText("Номер курса");
    createStudentGroupLineEdit = new QLineEdit(dialog);
    createStudentGroupLineEdit->setPlaceholderText("Номер группы");

    formLayout->addRow("Name:", createStudentNameLineEdit);
    formLayout->addRow("Date of Birth:", createStudentDOBLineEdit);
    formLayout->addRow("Grade:", createStudentGradeLineEdit);
    formLayout->addRow("Group:", createStudentGroupLineEdit);

    QPushButton *sendButton = new QPushButton("Send", dialog);
    connect(sendButton, &QPushButton::clicked, this, &ClientWindow::createStudentRequest);
    formLayout->addRow(sendButton);

    dialog->setLayout(formLayout);
    dialog->exec();
}

void ClientWindow::createStudentRequest() {
    QString name = createStudentNameLineEdit->text();
    QString dob = createStudentDOBLineEdit->text();
    QString grade = createStudentGradeLineEdit->text();
    QString group = createStudentGroupLineEdit->text();

    // Send request to create student
    QJsonObject json;
    json["name"] = name;
    json["date_of_birth"] = dob;
    json["grade"] = grade.toInt();
    json["student_group"] = group;

    QNetworkRequest request(QUrl("http://localhost:8000/students/"));
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QNetworkReply *reply = networkManager->post(request, QJsonDocument(json).toJson());
    connect(reply, &QNetworkReply::finished, reply, [this, reply]() {
        if (reply->error() == QNetworkReply::NoError) {
            QMessageBox::information(this, "Success", "Student created successfully");
            clearInputFields();
        } else {
            QMessageBox::warning(this, "Error", "Failed to create student");
        }
        reply->deleteLater();
    });
}

void ClientWindow::openUploadPhotoWindow() {
    QDialog *dialog = new QDialog(this);
    QVBoxLayout *layout = new QVBoxLayout(dialog);

    uploadPhotoStudentIDLineEdit = new QLineEdit(dialog);
    uploadPhotoStudentIDLineEdit->setPlaceholderText("ID студента");

    uploadPhotoSelectButton = new QPushButton("Select Photo", dialog);

    connect(uploadPhotoSelectButton, &QPushButton::clicked, [this, dialog]() {
        QString filePath = QFileDialog::getOpenFileName(this, "Select Photo", "", "Image Files (*.jpg *.png)");
            if (filePath.isEmpty()) {
                return;
            }
        QFile file(filePath);
        if (file.open(QIODevice::ReadOnly)) {
            imageData = file.readAll();
            uploadPhotoLabel->setText(QString("Photo selected: %1").arg(filePath));
            file.close();
        }
    });
    layout->addWidget(uploadPhotoStudentIDLineEdit);
    layout->addWidget(uploadPhotoSelectButton);

    uploadPhotoLabel = new QLabel("No photo selected", dialog);
    layout->addWidget(uploadPhotoLabel);

    QPushButton *sendButton = new QPushButton("Send", dialog);
    connect(sendButton, &QPushButton::clicked, this, &ClientWindow::uploadPhotoRequest);
    layout->addWidget(sendButton);

    dialog->setLayout(layout);
    dialog->exec();
}

void ClientWindow::uploadPhotoRequest() {
    QString studentID = uploadPhotoStudentIDLineEdit->text();

    if (imageData.isEmpty()) {
        QMessageBox::warning(this, "Error", "No photo selected");
        return;
    }

    QHttpMultiPart *multiPart = new QHttpMultiPart(QHttpMultiPart::FormDataType);
    QHttpPart imagePart;
    imagePart.setHeader(QNetworkRequest::ContentDispositionHeader, QVariant("form-data; name=\"photo\"; filename=\"photo.jpg\""));
    imagePart.setBody(imageData);
    multiPart->append(imagePart);

    QNetworkRequest request(QUrl(QString("http://localhost:8000/students/%1/photo").arg(studentID)));

    QNetworkReply *reply = networkManager->post(request, multiPart);
    multiPart->setParent(reply); // delete the multiPart with the reply

    connect(reply, &QNetworkReply::finished, reply, [this, reply]() {
        if (reply->error() == QNetworkReply::NoError) {
            QMessageBox::information(this, "Success", "Photo uploaded successfully");
            uploadPhotoStudentIDLineEdit->clear();
            uploadPhotoLabel->clear();
        } else {
            QMessageBox::warning(this, "Error", "Failed to upload photo: " + reply->errorString());
        }
        reply->deleteLater();
    });
}

void ClientWindow::readStudentsRequest() {
    // Send request to read students
    QNetworkRequest request(QUrl("http://localhost:8000/students/"));
    QNetworkReply *reply = networkManager->get(request);
    connect(reply, &QNetworkReply::finished, reply, [this, reply]() {
        if (reply->error() == QNetworkReply::NoError) {
            QByteArray responseData = reply->readAll();
            QJsonDocument jsonDocument = QJsonDocument::fromJson(responseData);
            QJsonArray students = jsonDocument.array();
            displayStudents(students);
        } else {
            QMessageBox::warning(this, "Error", "Failed to read students");
        }
        reply->deleteLater();
    });
}

void ClientWindow::displayStudents(const QJsonArray &students) {
    QDialog *dialog = new QDialog(this);
    QVBoxLayout *layout = new QVBoxLayout(dialog);

    QTableWidget *tableWidget = new QTableWidget(dialog);
    tableWidget->setRowCount(students.size());
    tableWidget->setColumnCount(5);
    tableWidget->setHorizontalHeaderLabels({"ID", "Name", "Date of Birth", "Grade", "Group"});

    for (int i = 0; i < students.size(); i++) {
        QJsonObject student = students.at(i).toObject();
        QTableWidgetItem *idItem = new QTableWidgetItem(student["id"].toString());
        QTableWidgetItem *nameItem = new QTableWidgetItem(student["name"].toString());
        QTableWidgetItem *dobItem = new QTableWidgetItem(student["date_of_birth"].toString());
        QTableWidgetItem *gradeItem = new QTableWidgetItem(student["grade"].toString());
        QTableWidgetItem *groupItem = new QTableWidgetItem(student["group"].toString());

        tableWidget->setItem(i, 0, idItem);
        tableWidget->setItem(i, 1, nameItem);
        tableWidget->setItem(i, 2, dobItem);
        tableWidget->setItem(i, 3, gradeItem);
        tableWidget->setItem(i, 4, groupItem);
    }
    layout->addWidget(tableWidget);
    dialog->setLayout(layout);
    dialog->exec();
}

void ClientWindow::openReadStudentWindow() {
    QDialog *dialog = new QDialog(this);
    QVBoxLayout *layout = new QVBoxLayout(dialog);

    readStudentIDLineEdit = new QLineEdit(dialog);
    readStudentIDLineEdit->setPlaceholderText("ID студента");

    QPushButton *sendButton = new QPushButton("Send", dialog);
    connect(sendButton, &QPushButton::clicked, this, &ClientWindow::readStudentRequest);

    layout->addWidget(readStudentIDLineEdit);
    layout->addWidget(sendButton);

    dialog->setLayout(layout);
    dialog->exec();
}

void ClientWindow::readStudentRequest() {
    QString studentID = readStudentIDLineEdit->text();
    QNetworkRequest request(QUrl(QString("http://localhost:8000/students/%1").arg(studentID)));
    QNetworkReply *reply = networkManager->get(request);
    connect(reply, &QNetworkReply::finished, reply, [this, reply]() {
        if (reply->error() == QNetworkReply::NoError) {
            QByteArray responseData = reply->readAll();
            QJsonObject student = QJsonDocument::fromJson(responseData).object();
            displayStudent(student);
        } else {
            QMessageBox::warning(this, "Error", "Failed to fetch student");
        }
        reply->deleteLater();
    });
}

void ClientWindow::displayStudent(const QJsonObject &student) {
    QDialog *dialog = new QDialog(this);
    QVBoxLayout *layout = new QVBoxLayout(dialog);

    QLabel *idLabel = new QLabel("ID: " + student["id"].toString(), dialog);
    QLabel *nameLabel = new QLabel("Name: " + student["name"].toString(), dialog);
    QLabel *dobLabel = new QLabel("Date of Birth: " + student["date_of_birth"].toString(), dialog);
    QLabel *gradeLabel = new QLabel("grade: " + QString::number(student["grade"].toInt()), dialog);
    QLabel *groupLabel = new QLabel("group: " + student["group"].toString(), dialog);

    QByteArray photoData = QByteArray::fromBase64(student["photo"].toString().toUtf8());
    QPixmap photoPixmap;
    photoPixmap.loadFromData(photoData);
    QLabel *photoLabel = new QLabel(dialog);
    photoLabel->setPixmap(photoPixmap.scaled(100, 100, Qt::KeepAspectRatio));

    layout->addWidget(idLabel);
    layout->addWidget(nameLabel);
    layout->addWidget(dobLabel);
    layout->addWidget(gradeLabel);
    layout->addWidget(groupLabel);
    layout->addWidget(photoLabel);

    dialog->setLayout(layout);
    dialog->exec();
}

void ClientWindow::openDeleteStudentWindow() {
    QDialog *dialog = new QDialog(this);
    QVBoxLayout *layout = new QVBoxLayout(dialog);

    deleteStudentIDLineEdit = new QLineEdit(dialog);
    deleteStudentIDLineEdit->setPlaceholderText("ID студента");

    QPushButton *sendButton = new QPushButton("Send", dialog);
    connect(sendButton, &QPushButton::clicked, this, &ClientWindow::deleteStudentRequest);

    layout->addWidget(deleteStudentIDLineEdit);
    layout->addWidget(sendButton);

    dialog->setLayout(layout);
    dialog->exec();
}

void ClientWindow::deleteStudentRequest() {
    QString studentID = deleteStudentIDLineEdit->text();
    QNetworkRequest request(QUrl(QString("http://localhost:8000/students/%1").arg(studentID)));
    QNetworkReply *reply = networkManager->deleteResource(request);
    connect(reply, &QNetworkReply::finished, reply, [this, reply]() {
        if (reply->error() == QNetworkReply::NoError) {
            QMessageBox::information(this, "Success", "Student deleted successfully");
            deleteStudentIDLineEdit->clear();
        } else {
            QMessageBox::warning(this, "Error", "Failed to delete student");
        }
        reply->deleteLater();
    });
}

void ClientWindow::clearInputFields() {
    createStudentNameLineEdit->clear();
    createStudentDOBLineEdit->clear();
    createStudentGradeLineEdit->clear();
    createStudentGroupLineEdit->clear();
}

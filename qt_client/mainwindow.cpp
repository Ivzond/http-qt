#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QJsonObject>
#include <QJsonDocument>
#include <QFileDialog>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    manager = new QNetworkAccessManager(this);
    connect(manager, &QNetworkAccessManager::finished, this, &MainWindow::replyFinished);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::createStudent() {
    QNetworkRequest request(QUrl("http://localhost:8000/students/"));
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    // Create JSON data for student
    QJsonObject studentObject;
    studentObject["name"] = ui->lineEditName->text();
    studentObject["date_of_birth"] = ui->dateOfBirthEdit->text();
    studentObject["grade"] = ui->spinBoxGrade->value();
    studentObject["student_group"] = ui->lineEditGroup->text();

    QJsonDocument doc(studentObject);
    QByteArray data = doc.toJson();

    manager->post(request, data);
}

void MainWindow::uploadPhoto() {
    QString filePath = QFileDialog::getOpenFileName(this, tr("Open Image File"), QString(), tr("Images (*.png *.jpg *.jpeg)"));
    if (!filePath.isEmpty()) {
        QNetworkRequest request(QUrl("http://localhost:8000/students/" + QString::number(ui->spinBoxStudentId->value()) + "/photo"));
        QHttpMultiPart *multiPart = new QHttpMultiPart(QHttpMultiPart::FormDataType);

        QHttpPart imagePart;
        imagePart.setHeader(QNetworkRequest::ContentTypeHeader, QVariant("image/jpeg"));
        imagePart.setHeader(QNetworkRequest::ContentDispositionHeader, QVariant("form-data; name=\"photo\"; filename=\"" + QFileInfo(filePath).fileName() + "\""));
        QFile *file = new QFile(filePath);
        file->open(QIODevice::ReadOnly);
        imagePart.setBodyDevice(file);
        file->setParent(multiPart);
        multiPart->append(imagePart);

        manager->post(request, multiPart);
    }
}

void MainWindow::readStudents() {
    QNetworkRequest request(QUrl("http://localhost:8000/students/"));

    manager->get(request);
}

void MainWindow::deleteStudent() {
    QNetworkRequest request(QUrl("http://localhost:8000/students/" + QString::number(ui->spinBoxStudentId->value())));

    manager->deleteResource(request);
}

void MainWindow::replyFinished(QNetworkReply *reply) {
    if (reply->error() == QNetworkReply::NoError) {
        QByteArray responseData = reply->readAll();
        qDebug() << "Response:" << responseData;
    } else {
        qDebug() << "Error:" << reply->errorString();
    }
    reply->deleteLater();
}



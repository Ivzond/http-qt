#include "clientwindow.h"
#include <QVBoxLayout>
#include <QFormLayout>
#include <QJsonObject>
#include <QHttpMultiPart>
#include <QImageIOHandler>
#include <QFile>
#include <QTextStream>
#include <QDateTime>

Q_LOGGING_CATEGORY(network, "network");

ClientWindow::ClientWindow(QWidget *parent) : QWidget(parent) {
    createStudentButton = new QPushButton("Создать запись о студенте", this);
    uploadPhotoButton = new QPushButton("Загрузить фото студента", this);
    readStudentsButton = new QPushButton("Прочитать записи о студентах", this);
    readStudentButton = new QPushButton("Прочитать запись о студенте", this);
    deleteStudentButton = new QPushButton("Удалить запись о студенте", this);

    connect(createStudentButton, &QPushButton::clicked, this, &ClientWindow::openCreateStudentWindow);
    connect(uploadPhotoButton, &QPushButton::clicked, this, &ClientWindow::openUploadPhotoWindow);
    connect(readStudentsButton, &QPushButton::clicked, this, &ClientWindow::openReadStudentsWindow);
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
    loadSettings();
}

void ClientWindow::loadSettings() {
    configFilePath = QFileDialog::getOpenFileName(this,
    "Выбрать конфигурационный файл", "", "Config files (*.ini);;All files (*.*)");
    if (!configFilePath.isEmpty()) {
        QSettings settings(configFilePath, QSettings::IniFormat);
        settings.beginGroup("CLIENT");
        username = settings.value("username").toString();
        passwordHash = settings.value("password_hash").toString();
        QString logPath = settings.value("log_path").toString();
        settings.endGroup();

        if (logPath.isEmpty()) {
            qCWarning(network) << "Log path not specified in config.ini";
            return;
        }

        QFile logFile(logPath);
        if (!logFile.open(QIODevice::WriteOnly | QIODevice::Append | QIODevice::Text)) {
            qCWarning(network) << "Failed to open log file at " << logPath;
            return;
        }

        QTextStream stream(&logFile);
        stream << "Logging started at " << QDateTime::currentDateTime().toString("yyyy-MM-dd HH:mm:ss") << "\n";
        logFile.close();

        qCInfo(network) << "Network logging initialized";
    } else {
        qWarning("No configuration file Selected");
        return;
    }
}

void ClientWindow::logMessage(const QString &message) {
    QSettings settings(configFilePath, QSettings::IniFormat);
    settings.beginGroup("CLIENT");
    QString logPath = settings.value("log_path").toString();
    settings.endGroup();

    QFile logFile(logPath);
    if (logFile.open(QIODevice::WriteOnly | QIODevice::Append | QIODevice::Text)) {
        QTextStream stream(&logFile);
        stream << QDateTime::currentDateTime().toString("yyyy-MM-dd HH:mm:ss") << " - " << message << "\n";
        logFile.close();
    }
}

void ClientWindow::openCreateStudentWindow() {
    QDialog *dialog = new QDialog(this);
    QFormLayout *formLayout = new QFormLayout(dialog);

    createStudentNameLineEdit = new QLineEdit(dialog);
    createStudentNameLineEdit->setPlaceholderText("Иванов И.И.");

    createStudentDOBEdit = new QDateEdit(dialog);
    createStudentDOBEdit->setDisplayFormat("ГГГГ-ММ-ДД");
    createStudentDOBEdit->setCalendarPopup(true);
    createStudentDOBEdit->setDate(QDate::currentDate());

    createStudentGradeLineEdit = new QLineEdit(dialog);
    createStudentGradeLineEdit->setPlaceholderText("Номер курса");
    createStudentGroupLineEdit = new QLineEdit(dialog);
    createStudentGroupLineEdit->setPlaceholderText("Номер группы");

    formLayout->addRow("Имя:", createStudentNameLineEdit);
    formLayout->addRow("Дата рождения:", createStudentDOBEdit);
    formLayout->addRow("Номер курса:", createStudentGradeLineEdit);
    formLayout->addRow("Номер группы:", createStudentGroupLineEdit);

    QPushButton *sendButton = new QPushButton("Создать запись", dialog);
    connect(sendButton, &QPushButton::clicked, this, &ClientWindow::createStudentRequest);
    formLayout->addRow(sendButton);

    dialog->setLayout(formLayout);
    dialog->exec();
}

void ClientWindow::createStudentRequest() {
    QString name = createStudentNameLineEdit->text();
    QString dob = createStudentDOBEdit->date().toString("yyyy-MM-dd");
    QString grade = createStudentGradeLineEdit->text();
    QString group = createStudentGroupLineEdit->text();

    QJsonObject json;
    json["name"] = name;
    json["date_of_birth"] = dob;
    json["grade"] = grade.toInt();
    json["student_group"] = group;

    QNetworkRequest request(QUrl("http://localhost:8000/students/"));
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QString credentials = QString("%1:%2").arg(username).arg(passwordHash);
    QByteArray authData = credentials.toUtf8().toBase64();
    request.setRawHeader("Authorization", "Basic " + authData);

    QNetworkReply *reply = networkManager->post(request, QJsonDocument(json).toJson());
    connect(reply, &QNetworkReply::finished, reply, [this, reply]() {
        if (reply->error() == QNetworkReply::NoError) {
            QMessageBox::information(this, "Отлично", "Запись успешно создана");
            clearInputFields();
            logMessage("Запись успешно создана");
        } else {
            QMessageBox::warning(this, "Ошибка", "Не удалось создать запись");
            logMessage("Не удалось создать запись: " + reply->errorString());
        }
        reply->deleteLater();
    });
}

void ClientWindow::openUploadPhotoWindow() {
    QDialog *dialog = new QDialog(this);
    QVBoxLayout *layout = new QVBoxLayout(dialog);

    uploadPhotoStudentIDLineEdit = new QLineEdit(dialog);
    uploadPhotoStudentIDLineEdit->setPlaceholderText("ID студента");

    uploadPhotoSelectButton = new QPushButton("Выбрать фото", dialog);

    connect(uploadPhotoSelectButton, &QPushButton::clicked, [this, dialog]() {
        QString filePath = QFileDialog::getOpenFileName(this, "Выбрать фото", "", "Image Files (*.jpg *.png)");
            if (filePath.isEmpty()) {
                return;
            }
        QFile file(filePath);
        if (file.open(QIODevice::ReadOnly)) {
            imageData = file.readAll();
            uploadPhotoLabel->setText(QString("Фото выбрано: %1").arg(filePath));
            file.close();
        }
    });
    layout->addWidget(uploadPhotoStudentIDLineEdit);
    layout->addWidget(uploadPhotoSelectButton);

    uploadPhotoLabel = new QLabel("Фото не выбрано", dialog);
    layout->addWidget(uploadPhotoLabel);

    QPushButton *sendButton = new QPushButton("Загрузить фотографию", dialog);
    connect(sendButton, &QPushButton::clicked, this, &ClientWindow::uploadPhotoRequest);
    layout->addWidget(sendButton);

    dialog->setLayout(layout);
    dialog->exec();
}

void ClientWindow::uploadPhotoRequest() {
    QString studentID = uploadPhotoStudentIDLineEdit->text();

    if (imageData.isEmpty()) {
        QMessageBox::warning(this, "Error", "Фото не выбрано");
        return;
    }

    QHttpMultiPart *multiPart = new QHttpMultiPart(QHttpMultiPart::FormDataType);
    QHttpPart imagePart;
    imagePart.setHeader(QNetworkRequest::ContentDispositionHeader, QVariant("form-data; name=\"photo\"; filename=\"photo.jpg\""));
    imagePart.setBody(imageData);
    multiPart->append(imagePart);

    QNetworkRequest request(QUrl(QString("http://localhost:8000/students/%1/photo").arg(studentID)));
    QString credentials = QString("%1:%2").arg(username).arg(passwordHash);
    QByteArray authData = credentials.toUtf8().toBase64();
    request.setRawHeader("Authorization", "Basic " + authData);

    QNetworkReply *reply = networkManager->post(request, multiPart);
    multiPart->setParent(reply); // delete the multiPart with the reply

    connect(reply, &QNetworkReply::finished, reply, [this, reply]() {
        if (reply->error() == QNetworkReply::NoError) {
            QMessageBox::information(this, "Отлично", "Фото успешно загружено");
            uploadPhotoStudentIDLineEdit->clear();
            uploadPhotoLabel->clear();
            logMessage("Фото успешно загружено");
        } else {
            QMessageBox::warning(this, "Ошибка", "Не удалось загрузить фото: " + reply->errorString());
            logMessage("Не удалось загрузить фото: " + reply->errorString());
        }
        reply->deleteLater();
    });
}

void ClientWindow::openReadStudentsWindow() {
    QDialog *dialog = new QDialog(this);
    QVBoxLayout *layout = new QVBoxLayout(dialog);

    readStudentsFilterNameLineEdit = new QLineEdit(dialog);
    readStudentsFilterNameLineEdit->setPlaceholderText("Фильтр по имени студента");

    readStudentsFilterGroupLineEdit = new QLineEdit(dialog);
    readStudentsFilterGroupLineEdit->setPlaceholderText("Фильтр по номеру группы");

    QPushButton *filterButton = new QPushButton("Применить фильтр", dialog);
    connect(filterButton, &QPushButton::clicked, this, &ClientWindow::readStudentsRequest);

    layout->addWidget(readStudentsFilterNameLineEdit);
    layout->addWidget(readStudentsFilterGroupLineEdit);
    layout->addWidget(filterButton);

    dialog->setLayout(layout);
    dialog->exec();
}

void ClientWindow::readStudentsRequest() {
    QNetworkRequest request(QUrl("http://localhost:8000/students/"));

    QString credentials = QString("%1:%2").arg(username).arg(passwordHash);
    QByteArray authData = credentials.toUtf8().toBase64();
    request.setRawHeader("Authorization", "Basic " + authData);

    QNetworkReply *reply = networkManager->get(request);
    connect(reply, &QNetworkReply::finished, reply, [this, reply]() {
        if (reply->error() == QNetworkReply::NoError) {
            QByteArray responseData = reply->readAll();
            QJsonDocument jsonDocument = QJsonDocument::fromJson(responseData);
            QJsonArray students = jsonDocument.array();
            displayStudents(students);
            readStudentsFilterNameLineEdit->clear();
            readStudentsFilterGroupLineEdit->clear();
            logMessage("Записи успешно прочитаны");
        } else {
            QMessageBox::warning(this, "Ошибка", "Не удалось прочитать записи");
            logMessage("Не удалось прочитать записи: " + reply->errorString());
        }
        reply->deleteLater();
    });
}

void ClientWindow::displayStudents(const QJsonArray &students) {
    QDialog *dialog = new QDialog(this);
    QVBoxLayout *layout = new QVBoxLayout(dialog);

    QString filterName = readStudentsFilterNameLineEdit->text();
    QString filterGroup = readStudentsFilterGroupLineEdit->text();

    QTableWidget *tableWidget = new QTableWidget(dialog);
    tableWidget->setRowCount(0);
    tableWidget->setColumnCount(6);
    tableWidget->setHorizontalHeaderLabels({"ID", "Имя", "Фото", "Дата рождения", "Курс", "Номер группы"});

    for (int i = 0; i < students.size(); i++) {
        QJsonObject student = students.at(i).toObject();
        QString studentName = student["name"].toString();
        QString studentGroup = student["student_group"].toString();

        if ((!filterName.isEmpty() && studentName != filterName) || (!filterGroup.isEmpty() && studentGroup != filterGroup)) {
            continue;
        }

        int row = tableWidget->rowCount();
        tableWidget->insertRow(row);

        QTableWidgetItem *idItem = new QTableWidgetItem(QString::number(student["id"].toInt()));
        QTableWidgetItem *nameItem = new QTableWidgetItem(student["name"].toString());
        QTableWidgetItem *dobItem = new QTableWidgetItem(student["date_of_birth"].toString());
        QTableWidgetItem *gradeItem = new QTableWidgetItem(QString::number(student["grade"].toInt()));
        QTableWidgetItem *groupItem = new QTableWidgetItem(student["student_group"].toString());

        QByteArray photoData = QByteArray::fromBase64(student["photo"].toString().toUtf8());
        QImage image;
        image.loadFromData(photoData);
        image = image.convertToFormat(QImage::Format_RGB888);

        QLabel *photoLabel = new QLabel;
        photoLabel->setPixmap(QPixmap::fromImage(image).scaled(100, 100, Qt::KeepAspectRatio));

        tableWidget->setItem(row, 0, idItem);
        tableWidget->setItem(row, 1, nameItem);
        tableWidget->setCellWidget(row, 2, photoLabel);
        tableWidget->setItem(row, 3, dobItem);
        tableWidget->setItem(row, 4, gradeItem);
        tableWidget->setItem(row, 5, groupItem);
    }
    tableWidget->resizeColumnsToContents();
    tableWidget->resizeRowsToContents();
    QSize tableSize = tableWidget->sizeHint();
    QSize minSize = QSize(qMax(800, tableSize.width()), qMax(600, tableSize.height()));
    dialog->setMinimumSize(minSize);

    layout->addWidget(tableWidget);
    dialog->setLayout(layout);
    dialog->exec();
}

void ClientWindow::openReadStudentWindow() {
    QDialog *dialog = new QDialog(this);
    QVBoxLayout *layout = new QVBoxLayout(dialog);

    readStudentIDLineEdit = new QLineEdit(dialog);
    readStudentIDLineEdit->setPlaceholderText("ID студента");

    QPushButton *sendButton = new QPushButton("Прочитать запись", dialog);
    connect(sendButton, &QPushButton::clicked, this, &ClientWindow::readStudentRequest);

    layout->addWidget(readStudentIDLineEdit);
    layout->addWidget(sendButton);

    dialog->setLayout(layout);
    dialog->exec();
}

void ClientWindow::readStudentRequest() {
    QString studentID = readStudentIDLineEdit->text();
    QNetworkRequest request(QUrl(QString("http://localhost:8000/students/%1").arg(studentID)));
    QString credentials = QString("%1:%2").arg(username).arg(passwordHash);
    QByteArray authData = credentials.toUtf8().toBase64();
    request.setRawHeader("Authorization", "Basic " + authData);

    QNetworkReply *reply = networkManager->get(request);
    connect(reply, &QNetworkReply::finished, reply, [this, reply]() {
        if (reply->error() == QNetworkReply::NoError) {
            QByteArray responseData = reply->readAll();
            QJsonObject student = QJsonDocument::fromJson(responseData).object();
            displayStudent(student);
            readStudentIDLineEdit->clear();
            logMessage("Запись успешно прочитана: " + student["name"].toString());
        } else {
            QMessageBox::warning(this, "Ошибка", "Не удалось прочитать запись");
            logMessage("Не удалось прочитать запись: " + reply->errorString());
        }
        reply->deleteLater();
    });
}

void ClientWindow::displayStudent(const QJsonObject &student) {
    QDialog *dialog = new QDialog(this);
    QVBoxLayout *layout = new QVBoxLayout(dialog);

    QLabel *idLabel = new QLabel("ID: " + QString::number(student["id"].toInt()), dialog);
    QLabel *nameLabel = new QLabel("Имя: " + student["name"].toString(), dialog);
    QLabel *dobLabel = new QLabel("Дата рождения: " + student["date_of_birth"].toString(), dialog);
    QLabel *gradeLabel = new QLabel("Курс: " + QString::number(student["grade"].toInt()), dialog);
    QLabel *groupLabel = new QLabel("Номер группы: " + student["student_group"].toString(), dialog);

    QByteArray photoData = QByteArray::fromBase64(student["photo"].toString().toUtf8());
    QImage image;
    image.loadFromData(photoData);
    image = image.convertToFormat(QImage::Format_RGB888);

    QLabel *photoLabel = new QLabel(dialog);
    photoLabel->setPixmap(QPixmap::fromImage(image).scaled(150, 150, Qt::KeepAspectRatio));

    layout->addWidget(idLabel);
    layout->addWidget(nameLabel);
    layout->addWidget(photoLabel);
    layout->addWidget(dobLabel);
    layout->addWidget(gradeLabel);
    layout->addWidget(groupLabel);

    dialog->setLayout(layout);
    dialog->exec();
}

void ClientWindow::openDeleteStudentWindow() {
    QDialog *dialog = new QDialog(this);
    QVBoxLayout *layout = new QVBoxLayout(dialog);

    deleteStudentIDLineEdit = new QLineEdit(dialog);
    deleteStudentIDLineEdit->setPlaceholderText("ID студента");

    QPushButton *sendButton = new QPushButton("Отправить", dialog);
    connect(sendButton, &QPushButton::clicked, this, &ClientWindow::deleteStudentRequest);

    layout->addWidget(deleteStudentIDLineEdit);
    layout->addWidget(sendButton);

    dialog->setLayout(layout);
    dialog->exec();
}

void ClientWindow::deleteStudentRequest() {
    QString studentID = deleteStudentIDLineEdit->text();
    QNetworkRequest request(QUrl(QString("http://localhost:8000/students/%1").arg(studentID)));
    QString credentials = QString("%1:%2").arg(username).arg(passwordHash);
    QByteArray authData = credentials.toUtf8().toBase64();
    request.setRawHeader("Authorization", "Basic " + authData);

    QNetworkReply *reply = networkManager->deleteResource(request);
    connect(reply, &QNetworkReply::finished, reply, [this, reply]() {
        if (reply->error() == QNetworkReply::NoError) {
            QMessageBox::information(this, "Отлично", "Запись успешно удалена");
            deleteStudentIDLineEdit->clear();
            logMessage("Запись успешно удалена");
        } else {
            QMessageBox::warning(this, "Ошибка", "Не удалось удалить студента");
            logMessage("Ошибка при удалении записи");
        }
        reply->deleteLater();
    });
}

void ClientWindow::clearInputFields() {
    createStudentNameLineEdit->clear();
    createStudentDOBEdit->clear();
    createStudentGradeLineEdit->clear();
    createStudentGroupLineEdit->clear();
}

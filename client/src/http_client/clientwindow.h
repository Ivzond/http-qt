#ifndef CLIENTWINDOW_H
#define CLIENTWINDOW_H

#include <QWidget>
#include <QPushButton>
#include <QLineEdit>
#include <QDateEdit>
#include <QLabel>
#include <QFileDialog>
#include <QMessageBox>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QJsonDocument>
#include <QJsonArray>
#include <QTableWidget>
#include <QSettings>
#include <QLoggingCategory>

class ClientWindow : public QWidget {
    Q_OBJECT
public:
    explicit ClientWindow(QWidget *parent = nullptr);

private slots:
    void openCreateStudentWindow();
    void createStudentRequest();
    void openUploadPhotoWindow();
    void uploadPhotoRequest();
    void openReadStudentsWindow();
    void readStudentsRequest();
    void openReadStudentWindow();
    void readStudentRequest();
    void openDeleteStudentWindow();
    void deleteStudentRequest();

private:
    QPushButton *createStudentButton;
    QPushButton *uploadPhotoButton;
    QPushButton *readStudentsButton;
    QPushButton *readStudentButton;
    QPushButton *deleteStudentButton;

    QLineEdit *createStudentNameLineEdit;
    QDateEdit *createStudentDOBEdit;
    QLineEdit *createStudentGradeLineEdit;
    QLineEdit *createStudentGroupLineEdit;
    QLineEdit *uploadPhotoStudentIDLineEdit;
    QLineEdit *readStudentsFilterNameLineEdit;
    QLineEdit *readStudentsFilterGroupLineEdit;
    QLineEdit *readStudentIDLineEdit;
    QLineEdit *deleteStudentIDLineEdit;

    QPushButton *uploadPhotoSelectButton;
    QLabel *uploadPhotoLabel;
    QByteArray imageData;

    QNetworkAccessManager *networkManager;
    QString username;
    QString passwordHash;
    QString configFilePath;

    void clearInputFields();
    void displayStudents(const QJsonArray &students);
    void displayStudent(const QJsonObject &student);
    void loadSettings();
    void logMessage(const QString &message);
};

#endif // CLIENTWINDOW_H

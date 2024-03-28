#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "QtNetwork"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void createStudent();
    void uploadPhoto();
    void readStudents();
    void deleteStudent();
    void openStudentCreationDialog();
    void handleStudentCreation();
    void replyFinished(QNetworkReply *reply);

//    void on_pushButton_clicked();

private:
    Ui::MainWindow *ui;
    QNetworkAccessManager *manager;
};
#endif // MAINWINDOW_H

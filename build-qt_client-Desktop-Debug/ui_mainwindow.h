/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.15.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDateEdit>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSpinBox>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralwidget;
    QWidget *verticalLayoutWidget;
    QVBoxLayout *verticalLayout;
    QPushButton *CreateStudentButton;
    QPushButton *UploadStudentsButton;
    QPushButton *ReadStudentsButton;
    QPushButton *ReadStudentButton;
    QPushButton *DeleteButtonButton;
    QWidget *verticalLayoutWidget_2;
    QVBoxLayout *verticalLayout_2;
    QLineEdit *lineEditName;
    QDateEdit *dateOfBirthEdit;
    QLineEdit *lineEditGroup;
    QSpinBox *spinBoxGrade;
    QPushButton *pushButton_6;
    QWidget *verticalLayoutWidget_3;
    QVBoxLayout *verticalLayout_3;
    QSpinBox *spinBoxStudentId;
    QMenuBar *menubar;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(800, 600);
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName(QString::fromUtf8("centralwidget"));
        verticalLayoutWidget = new QWidget(centralwidget);
        verticalLayoutWidget->setObjectName(QString::fromUtf8("verticalLayoutWidget"));
        verticalLayoutWidget->setGeometry(QRect(20, 30, 170, 201));
        verticalLayout = new QVBoxLayout(verticalLayoutWidget);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        verticalLayout->setContentsMargins(0, 0, 0, 0);
        CreateStudentButton = new QPushButton(verticalLayoutWidget);
        CreateStudentButton->setObjectName(QString::fromUtf8("CreateStudentButton"));

        verticalLayout->addWidget(CreateStudentButton);

        UploadStudentsButton = new QPushButton(verticalLayoutWidget);
        UploadStudentsButton->setObjectName(QString::fromUtf8("UploadStudentsButton"));

        verticalLayout->addWidget(UploadStudentsButton);

        ReadStudentsButton = new QPushButton(verticalLayoutWidget);
        ReadStudentsButton->setObjectName(QString::fromUtf8("ReadStudentsButton"));

        verticalLayout->addWidget(ReadStudentsButton);

        ReadStudentButton = new QPushButton(verticalLayoutWidget);
        ReadStudentButton->setObjectName(QString::fromUtf8("ReadStudentButton"));

        verticalLayout->addWidget(ReadStudentButton);

        DeleteButtonButton = new QPushButton(verticalLayoutWidget);
        DeleteButtonButton->setObjectName(QString::fromUtf8("DeleteButtonButton"));

        verticalLayout->addWidget(DeleteButtonButton);

        verticalLayoutWidget_2 = new QWidget(centralwidget);
        verticalLayoutWidget_2->setObjectName(QString::fromUtf8("verticalLayoutWidget_2"));
        verticalLayoutWidget_2->setGeometry(QRect(200, 30, 160, 153));
        verticalLayout_2 = new QVBoxLayout(verticalLayoutWidget_2);
        verticalLayout_2->setObjectName(QString::fromUtf8("verticalLayout_2"));
        verticalLayout_2->setContentsMargins(0, 0, 0, 0);
        lineEditName = new QLineEdit(verticalLayoutWidget_2);
        lineEditName->setObjectName(QString::fromUtf8("lineEditName"));

        verticalLayout_2->addWidget(lineEditName);

        dateOfBirthEdit = new QDateEdit(verticalLayoutWidget_2);
        dateOfBirthEdit->setObjectName(QString::fromUtf8("dateOfBirthEdit"));

        verticalLayout_2->addWidget(dateOfBirthEdit);

        lineEditGroup = new QLineEdit(verticalLayoutWidget_2);
        lineEditGroup->setObjectName(QString::fromUtf8("lineEditGroup"));

        verticalLayout_2->addWidget(lineEditGroup);

        spinBoxGrade = new QSpinBox(verticalLayoutWidget_2);
        spinBoxGrade->setObjectName(QString::fromUtf8("spinBoxGrade"));

        verticalLayout_2->addWidget(spinBoxGrade);

        pushButton_6 = new QPushButton(verticalLayoutWidget_2);
        pushButton_6->setObjectName(QString::fromUtf8("pushButton_6"));

        verticalLayout_2->addWidget(pushButton_6);

        verticalLayoutWidget_3 = new QWidget(centralwidget);
        verticalLayoutWidget_3->setObjectName(QString::fromUtf8("verticalLayoutWidget_3"));
        verticalLayoutWidget_3->setGeometry(QRect(200, 200, 160, 41));
        verticalLayout_3 = new QVBoxLayout(verticalLayoutWidget_3);
        verticalLayout_3->setObjectName(QString::fromUtf8("verticalLayout_3"));
        verticalLayout_3->setContentsMargins(0, 0, 0, 0);
        spinBoxStudentId = new QSpinBox(verticalLayoutWidget_3);
        spinBoxStudentId->setObjectName(QString::fromUtf8("spinBoxStudentId"));

        verticalLayout_3->addWidget(spinBoxStudentId);

        MainWindow->setCentralWidget(centralwidget);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName(QString::fromUtf8("menubar"));
        menubar->setGeometry(QRect(0, 0, 800, 22));
        MainWindow->setMenuBar(menubar);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName(QString::fromUtf8("statusbar"));
        MainWindow->setStatusBar(statusbar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        CreateStudentButton->setText(QCoreApplication::translate("MainWindow", "Create student", nullptr));
        UploadStudentsButton->setText(QCoreApplication::translate("MainWindow", "Upload student's photo", nullptr));
        ReadStudentsButton->setText(QCoreApplication::translate("MainWindow", "Read students", nullptr));
        ReadStudentButton->setText(QCoreApplication::translate("MainWindow", "Read student", nullptr));
        DeleteButtonButton->setText(QCoreApplication::translate("MainWindow", "Delete student", nullptr));
        lineEditName->setText(QString());
        pushButton_6->setText(QCoreApplication::translate("MainWindow", "Create", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H

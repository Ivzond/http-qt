#include "clientwindow.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    ClientWindow clientWindow;
    clientWindow.resize(400, 300);
    clientWindow.show();

    return app.exec();
}

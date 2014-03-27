#include "mainwindow.h"
#include "inputpage.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    InputPage w;
    w.show();

    return a.exec();
}

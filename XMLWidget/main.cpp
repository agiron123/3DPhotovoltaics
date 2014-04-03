#include "mainwindow.h"
#include "inputpage.h"
#include <QApplication>
#include <QDebug>

int main(int argc, char *argv[])
{
    qDebug() << "Application starting ... ";
    QApplication a(argc, argv);
    InputPage w;

    w.show();
    return a.exec();
}

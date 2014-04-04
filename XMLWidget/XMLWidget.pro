#-------------------------------------------------
#
# Project created by QtCreator 2014-03-25T15:12:32
#
#-------------------------------------------------

QT       += core gui
QT       += uitools
QT       += opengl xml


greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = XMLWidget
TEMPLATE = app


SOURCES += main.cpp \
        mainwindow.cpp \
        inputpage.cpp \

HEADERS  += mainwindow.h \
         inputpage.h \

FORMS    += mainwindow.ui \
         inputpage.ui \

CONFIG += console

CONFIG   -= x86_64

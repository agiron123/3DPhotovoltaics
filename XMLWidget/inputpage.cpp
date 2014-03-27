#include "inputpage.h"
#include "ui_inputpage.h"

InputPage::InputPage(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::InputPage)
{
    ui->setupUi(this);
}

InputPage::~InputPage()
{
    delete ui;
}

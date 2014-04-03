#ifndef INPUTPAGE_H
#define INPUTPAGE_H

#include <QDialog>
#include <QWidget>
#include <QCheckBox>

namespace Ui {
class InputPage;
}

class InputPage : public QDialog
{
    Q_OBJECT

public:
    explicit InputPage(QWidget *parent = 0);
    ~InputPage();
    QWidget* loadUiFile();


private slots:
    void on_pushButton_10_clicked(bool checked);


private:
    Ui::InputPage *ui;
    QCheckBox power_genRatioCheckbox;
};

#endif // INPUTPAGE_H


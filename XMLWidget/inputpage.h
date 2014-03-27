#ifndef INPUTPAGE_H
#define INPUTPAGE_H

#include <QDialog>

namespace Ui {
class InputPage;
}

class InputPage : public QDialog
{
    Q_OBJECT

public:
    explicit InputPage(QWidget *parent = 0);
    ~InputPage();

private:
    Ui::InputPage *ui;
};

#endif // INPUTPAGE_H

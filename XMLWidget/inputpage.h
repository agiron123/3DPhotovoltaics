#ifndef INPUTPAGE_H
#define INPUTPAGE_H

#include <QDialog>
#include <QWidget>
#include <QCheckBox>
#include <QDomElement>

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
    QDomElement addElement( QDomDocument &doc, QDomNode &node,
                            const QString &tag,
                            const QString &value = QString::null );



private slots:
    void on_pushButton_10_clicked(bool checked);


private:
    Ui::InputPage *ui;
    QCheckBox power_genRatioCheckbox;
};

#endif // INPUTPAGE_H


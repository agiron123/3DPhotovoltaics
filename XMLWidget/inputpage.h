#ifndef INPUTPAGE_H
#define INPUTPAGE_H

#include <QDialog>
#include <QWidget>
#include <QCheckBox>
#include <QDomElement>
#include <QTabWidget>
#include <QLineEdit>
#include <QPlainTextEdit>
#include <QComboBox>

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
    void on_addSimulationButton_clicked();
    bool validateFormInput();

    void on_doneButton_clicked();

private:
    Ui::InputPage *ui;
    QCheckBox power_genRatioCheckbox;
    QTabWidget* root;

    //General Properties Tab
    QWidget* generalPropertiesTab;
    QLineEdit* panel_orientationEdit;
    QCheckBox* specularReflectionCheckBox;

    //Orbital Properties Tab
    QWidget* orbitalPropertiesTab;
    QPlainTextEdit* tlePlainTextEdit;
    QLineEdit* beta_angleEdit;
    QLineEdit* earthshineEdit;
    QLineEdit* orbitIntervalEdit;

    //Fixed Orbit
    QLineEdit* zenithAngleEdit;
    QLineEdit* azumithAngleEdit;
    QLineEdit* photonCountEdit;

    //Material Profiles Tab
    QWidget* materialProfilesTab;
    QCheckBox* absorptionCheckbox;
    QCheckBox* towerTopsCheckbox;
    QCheckBox* trappingCheckbox;
    QComboBox* shapeComboBox;
    QLineEdit* towerPitchEdit;
    QLineEdit* towerWidthEdit;
    QLineEdit* towerHeightEdit;

    //Output Settings
    QWidget* outputTab;
    QCheckBox* maxPointPowerVsZenithAngleCheckbox;
    QCheckBox* AverageReflectionsVsAzumithalCheckbox;
    QCheckBox* AspectRatioVsAverageReflectionsCheckbox;
    QCheckBox* IntegratedAreaRatioVsAvgNumReflectionsCheckbox;
    QCheckBox* PowerRatio3DVsAbsorbanceCheckbox;
    QCheckBox* AvgInteractionsVsTowerSpacingLogCheckbox;
    QCheckBox* AvgReflectionsVsTowerHeightCheckbox;
    QCheckBox* AbsorptionEfficiencyVsAzumithalCheckbox;
    QCheckBox* includePathsCheckbox;
};

#endif // INPUTPAGE_H


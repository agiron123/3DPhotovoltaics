#include "inputpage.h"
#include "ui_inputpage.h"
#include <QDebug>
#include <QtUiTools>
#include <QLineEdit>
#include <QTabWidget>
#include <QGroupBox>

InputPage::InputPage(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::InputPage)
{
    qDebug() << "Input Page UI Starting ...";
    QWidget test;
    ui->setupUi(this);

}

InputPage::~InputPage()
{
    delete ui;
}

QWidget* InputPage::loadUiFile()
{
    qDebug() << "Loading the UI file";

    QUiLoader loader;

    QFile file(":/forms/inputpage.ui");
    file.open(QFile::ReadOnly);

    QWidget *formWidget = loader.load(&file, this);
    file.close();

    QCheckBox* checkbox = loader.findChild<QCheckBox*>("powergenratio3D");
    checkbox->setChecked(true);

    qDebug() << "Hello there, I'm a log!";

    //After we did everything to the view, now update the view.
    formWidget->update();

    return formWidget;
}

void InputPage::on_pushButton_10_clicked(bool checked)
{
    QTabWidget* root = findChild<QTabWidget*>("tab_widget");

    //First load the general properties tab
    QWidget* generalPropertiesTab = root->findChild<QWidget*>("general_properties_tab");
    QLineEdit* panel_orientationEdit = generalPropertiesTab->findChild<QLineEdit*>("panel_orientation");
    QString panel_orientationString = panel_orientationEdit->text();
    qDebug() << "Panel Orientation: " + panel_orientationString; //verified

    //Specular_Reflection
    QCheckBox* specularReflectionCheckBox = generalPropertiesTab->findChild<QCheckBox*>("Non_Specular_Reflection");
    if(specularReflectionCheckBox->isChecked())
    {
        qDebug() << "Non-Specular Reflection: True"; //verified
    }
    else
    {
        qDebug() << "Non-Specular Reflection: False"; //verified
    }

    //Orbital Properties Tab (orbital_properties_tab
    QWidget* orbitalPropertiesTab = root->findChild<QWidget*>("orbital_properties_tab");
    QPlainTextEdit* tlePlainTextEdit = orbitalPropertiesTab->findChild<QPlainTextEdit*>("TLE");
    QString tlePlainTextEditString = tlePlainTextEdit->toPlainText();
    qDebug() << "TLE: " + tlePlainTextEditString; //verified

    //TODO: Access orbital properties form inputs here
    QLineEdit* beta_angleEdit = orbitalPropertiesTab->findChild<QLineEdit*>("beta_angle");
    QString beta_angleString = beta_angleEdit->text();
    qDebug() << "Beta Angle: " + beta_angleString; //verified

    QLineEdit* earthshineEdit = orbitalPropertiesTab->findChild<QLineEdit*>("earthshine");
    QString earthshineString = earthshineEdit->text();
    qDebug() << "Earthshine: " + earthshineString; //verified

    //orbit_interval
    QLineEdit* orbitIntervalEdit = orbitalPropertiesTab->findChild<QLineEdit*>("interval");
    QString orbitIntervalString = orbitIntervalEdit->text();
    qDebug() << "Orbit Interval: " + orbitIntervalString; //verified

    //Zenith Angle
    QLineEdit* zenithAngleEdit = orbitalPropertiesTab->findChild<QLineEdit*>("zenith_angle");
    QString zenithAngleString = zenithAngleEdit->text();
    qDebug() << "Zenith Angle: " + zenithAngleString; //verified

    //azimuth_angle
    QLineEdit* azumithAngleEdit = orbitalPropertiesTab->findChild<QLineEdit*>("azimuth_angle");
    QString azumithAngleString = azumithAngleEdit->text();
    qDebug() << "Azumith Angle: " + azumithAngleString; //verified

    //photon_count
    QLineEdit* photonCountEdit = orbitalPropertiesTab->findChild<QLineEdit*>("photon_count");
    QString photonCountString = photonCountEdit->text();
    qDebug() << "Photon Count: " + photonCountString; //verified

    //Material Profiles Tab
    QWidget* materialProfilesTab = root->findChild<QWidget*>("material_profiles_tab");

    //TODO: Access material profiles form inputs here

    //Absorptions
    QCheckBox* absorptionCheckbox = materialProfilesTab->findChild<QCheckBox*>("absorbing");
    if(absorptionCheckbox->isChecked())
    {
        qDebug() << "Absorption: True"; //verified
    }
    else
    {
        qDebug() << "Absorption: False"; //verified
    }

    //Tower tops
    QCheckBox* towerTopsCheckbox = materialProfilesTab->findChild<QCheckBox*>("tower_tops");
    if(towerTopsCheckbox->isChecked())
    {
        qDebug() << "Tower Tops: True"; //verified
    }
    else
    {
        qDebug() << "Tower Tops: False"; //verified
    }

    //Trapping
    QCheckBox* trappingCheckbox = materialProfilesTab->findChild<QCheckBox*>("trapping");
    if(trappingCheckbox->isChecked())
    {
        qDebug() << "Trapping: True"; //verified
    }
    else
    {
        qDebug() << "Trapping: False"; //verified
    }

    //Tower Shape
    //shape
    QComboBox* shapeComboBox = materialProfilesTab->findChild<QComboBox*>("shape");
    qDebug() << "Selected Shape: " + shapeComboBox->itemText(shapeComboBox->currentIndex());


    //Output Tab
    QWidget* outputTab = root->findChild<QWidget*>("output_tab");

    //TODO: Access output tab form input here
    //MaxPointPowerVsZenithAngle
    QCheckBox* maxPointPowerVsZenithAngleCheckbox = outputTab->findChild<QCheckBox*>("MaxPointPowerVsZenithAngle");
    if(maxPointPowerVsZenithAngleCheckbox->isChecked())
    {
        qDebug() << "MaxPointPowerVsZenithAngle: True"; //verified
    }
    else
    {
        qDebug() << "MaxPointPowerVsZenithAngle: False"; //verified
    }

    //AverageReflectionsVsAzumithal
    QCheckBox* AverageReflectionsVsAzumithalCheckbox = outputTab->findChild<QCheckBox*>("AverageReflectionsVsAzumithal");
    if(AverageReflectionsVsAzumithalCheckbox->isChecked())
    {
        qDebug() << "AverageReflectionsVsAzumithal: True"; //verified
    }
    else
    {
        qDebug() << "AverageReflectionsVsAzumithal: False"; //verified
    }

    //AbsorptionEfficiencyVsAzumithal
    QCheckBox* AbsorptionEfficiencyVsAzumithalCheckbox = outputTab->findChild<QCheckBox*>("AbsorptionEfficiencyVsAzumithal");
    if(AbsorptionEfficiencyVsAzumithalCheckbox->isChecked())
    {
        qDebug() << "AbsorptionEfficiencyVsAzumithal: True"; //verified
    }
    else
    {
        qDebug() << "AbsorptionEfficiencyVsAzumithal: False"; //verified
    }

    //AspectRatioVsAverageReflections
    QCheckBox* AspectRatioVsAverageReflectionsCheckbox = outputTab->findChild<QCheckBox*>("AspectRatioVsAverageReflections");
    if(AspectRatioVsAverageReflectionsCheckbox->isChecked())
    {
        qDebug() << "AspectRatioVsAverageReflections: True"; //verified
    }
    else
    {
        qDebug() << "AspectRatioVsAverageReflections: False"; //verified
    }

    //IntegratedAreaRatioVsAvgNumReflections
    QCheckBox* IntegratedAreaRatioVsAvgNumReflectionsCheckbox = outputTab->findChild<QCheckBox*>("IntegratedAreaRatioVsAvgNumReflections");
    if(IntegratedAreaRatioVsAvgNumReflectionsCheckbox->isChecked())
    {
        qDebug() << "IntegratedAreaRatioVsAvgNumReflections: True"; //verified
    }
    else
    {
        qDebug() << "IntegratedAreaRatioVsAvgNumReflections: False"; //verified
    }

    //PowerRatio3DVsAbsorbance
    QCheckBox* PowerRatio3DVsAbsorbanceCheckbox = outputTab->findChild<QCheckBox*>("PowerRatio3DVsAbsorbance");
    if(PowerRatio3DVsAbsorbanceCheckbox->isChecked())
    {
        qDebug() << "PowerRatio3DVsAbsorbance: True"; //verified
    }
    else
    {
        qDebug() << "PowerRatio3DVsAbsorbance: False"; //verified
    }

    //AvgInteractionsVsTowerSpacingLog
    QCheckBox* AvgInteractionsVsTowerSpacingLogCheckbox = outputTab->findChild<QCheckBox*>("AvgInteractionsVsTowerSpacingLog");
    if(AvgInteractionsVsTowerSpacingLogCheckbox->isChecked())
    {
        qDebug() << "AvgInteractionsVsTowerSpacingLog: True"; //verified
    }
    else
    {
        qDebug() << "AvgInteractionsVsTowerSpacingLog: False"; //verified
    }

    //AvgReflectionsVsTowerHeight
    QCheckBox* AvgReflectionsVsTowerHeightCheckbox = outputTab->findChild<QCheckBox*>("AvgReflectionsVsTowerHeight");
    if(AvgReflectionsVsTowerHeightCheckbox->isChecked())
    {
        qDebug() << "AvgReflectionsVsTowerHeight: True"; //verified
    }
    else
    {
        qDebug() << "AvgReflectionsVsTowerHeight: False"; //verified
    }


    //TODO: Remove this later
    if(checked)
    {
        qDebug() << "message, Pressed the damn button";
    }
}

#include "inputpage.h"
#include "ui_inputpage.h"
#include <QDebug>
#include <QtUiTools>
#include <QLineEdit>
#include <QTabWidget>
#include <QGroupBox>
#include <QDomElement>

InputPage::InputPage(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::InputPage)
{
    qDebug() << "Input Page UI Starting ...";
    QWidget test;
    ui->setupUi(this);

    //Initialize the member variables
    //General Properties Tab
    root = findChild<QTabWidget*>("tab_widget");
    generalPropertiesTab = root->findChild<QWidget*>("general_properties_tab");
    panel_orientationEdit = generalPropertiesTab->findChild<QLineEdit*>("panel_orientation");
    specularReflectionCheckBox = generalPropertiesTab->findChild<QCheckBox*>("Non_Specular_Reflection");

    //TODO: Add to xml document structure
    panelHeightEdit = generalPropertiesTab->findChild<QLineEdit*>("panel_height");
    panelWidthEdit = generalPropertiesTab->findChild<QLineEdit*>("panel_width");

    //Orbital Properties Tab
    orbitalPropertiesTab = root->findChild<QWidget*>("orbital_properties_tab");
    tlePlainTextEdit = orbitalPropertiesTab->findChild<QPlainTextEdit*>("TLE");
    beta_angleEdit = orbitalPropertiesTab->findChild<QLineEdit*>("beta_angle");
    earthshineEdit = orbitalPropertiesTab->findChild<QLineEdit*>("earthshine");

    //Fixed Orbit
    orbitIntervalEdit = orbitalPropertiesTab->findChild<QLineEdit*>("interval");
    zenithAngleEdit = orbitalPropertiesTab->findChild<QLineEdit*>("zenith_angle");
    azumithAngleEdit = orbitalPropertiesTab->findChild<QLineEdit*>("azimuth_angle");
    photonCountEdit = orbitalPropertiesTab->findChild<QLineEdit*>("photon_count");

    //Material Profiles Tab
    materialProfilesTab = root->findChild<QWidget*>("material_profiles_tab");
    absorptionCheckbox = materialProfilesTab->findChild<QCheckBox*>("absorbing");
    towerTopsCheckbox = materialProfilesTab->findChild<QCheckBox*>("tower_tops");
    trappingCheckbox = materialProfilesTab->findChild<QCheckBox*>("trapping");
    shapeComboBox = materialProfilesTab->findChild<QComboBox*>("shape");
    towerPitchEdit = materialProfilesTab->findChild<QLineEdit*>("pitch");
    towerWidthEdit = materialProfilesTab->findChild<QLineEdit*>("width");
    towerHeightEdit = materialProfilesTab->findChild<QLineEdit*>("height");

    //Output Tab
    outputTab = root->findChild<QWidget*>("output_tab");
    maxPointPowerVsZenithAngleCheckbox = outputTab->findChild<QCheckBox*>("MaxPointPowerVsZenithAngle");
    AverageReflectionsVsAzumithalCheckbox = outputTab->findChild<QCheckBox*>("AverageReflectionsVsAzumithal");
    AspectRatioVsAverageReflectionsCheckbox = outputTab->findChild<QCheckBox*>("AspectRatioVsAverageReflections");
    IntegratedAreaRatioVsAvgNumReflectionsCheckbox = outputTab->findChild<QCheckBox*>("IntegratedAreaRatioVsAvgNumReflections");
    PowerRatio3DVsAbsorbanceCheckbox = outputTab->findChild<QCheckBox*>("PowerRatio3DVsAbsorbance");
    AvgInteractionsVsTowerSpacingLogCheckbox = outputTab->findChild<QCheckBox*>("AvgInteractionsVsTowerSpacingLog");
    AvgReflectionsVsTowerHeightCheckbox = outputTab->findChild<QCheckBox*>("AvgReflectionsVsTowerHeight");
    AbsorptionEfficiencyVsAzumithalCheckbox = outputTab->findChild<QCheckBox*>("AbsorptionEfficiencyVsAzumithal");
    includePathsCheckbox = outputTab->findChild<QCheckBox*>("include_paths");
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

    //After we did everything to the view, now update the view.
    formWidget->update();

    return formWidget;
}

void InputPage::on_pushButton_10_clicked(bool checked)
{
    QDomDocument doc; //root element for the XML file
    QDomProcessingInstruction instr = doc.createProcessingInstruction(
                     "xml", "version='1.0' encoding='UTF-8'");
    doc.appendChild(instr);

    // generate configurations tag as root, and then add simulations to that configurations Element
    QDomElement configurationsElement = addElement( doc, doc, "configurations" );
    QDomElement simulationsElement = addElement(doc, configurationsElement, "simulation");

    //First load the general properties tab
    QString panel_orientationString = panel_orientationEdit->text();
    qDebug() << "Panel Orientation: " + panel_orientationString; //verified
    addElement(doc, simulationsElement, "panel_orientation", panel_orientationString);

    //Specular_Reflection
    if(specularReflectionCheckBox->isChecked())
    {
        qDebug() << "Non-Specular Reflection: True"; //verified
        addElement(doc, simulationsElement, "non_specular_reflection", "True");
    }
    else
    {
        qDebug() << "Non-Specular Reflection: False"; //verified
        addElement(doc, simulationsElement, "non_specular_reflection", "False");
    }

    ///////////////////////////////////////////Orbital Properties/////////////////////////////////////////////////////////////////////////

    //Orbital Properties Tab (orbital_properties_tab
    QString tlePlainTextEditString = tlePlainTextEdit->toPlainText();
    qDebug() << "TLE: " + tlePlainTextEditString; //verified

    QDomElement orbitalPropertiesElement = addElement(doc, simulationsElement, "orbital_properties");
    QDomElement realOrbitElement = addElement(doc, orbitalPropertiesElement, "real_orbit");

    QDomElement tle = addElement(doc, realOrbitElement, "tle", tlePlainTextEditString);
    //TODO: Parse out the lines that are entered and put them into these two tags.
    //addElement(doc, tle, "line1", "line1text");
    //addElement(doc, tle, "line2", "line2text");

    //beta_angle
    QString beta_angleString = beta_angleEdit->text();
    qDebug() << "Beta Angle: " + beta_angleString; //verified
    addElement(doc, realOrbitElement, "beta_angle", beta_angleString);

    //earthshine
    QString earthshineString = earthshineEdit->text();
    qDebug() << "Earthshine: " + earthshineString; //verified
    addElement(doc, realOrbitElement, "earthshine", earthshineString);

    //orbit_interval
    QString orbitIntervalString = orbitIntervalEdit->text();
    qDebug() << "Orbit Interval: " + orbitIntervalString; //verified
    addElement(doc, realOrbitElement, "interval", orbitIntervalString);

    ///////////////////////////////////////////Fixed Orbit/////////////////////////////////////////////////////////////////////////

    QDomElement fixedOrbitElement = addElement(doc, orbitalPropertiesElement, "tle", tlePlainTextEditString);

    //Zenith Angle
    QString zenithAngleString = zenithAngleEdit->text();
    qDebug() << "Zenith Angle: " + zenithAngleString; //verified
    addElement(doc, fixedOrbitElement, "zenith_angle", zenithAngleString);

    //azimuth_angle
    QString azumithAngleString = azumithAngleEdit->text();
    qDebug() << "Azumith Angle: " + azumithAngleString; //verified
    addElement(doc, fixedOrbitElement, "azimuth_angle", azumithAngleString);

    //photon_count
    QString photonCountString = photonCountEdit->text();
    qDebug() << "Photon Count: " + photonCountString; //verified
    addElement(doc, fixedOrbitElement, "photon_count", photonCountString);

    //////////////////////////////////////////END Fixed Orbit//////////////////////////////////////////////////////////////////////

    ///////////////////////////////////////////Material Profiles///////////////////////////////////////////////////////////////////

    QDomElement materialProfileElement = addElement(doc, simulationsElement, "material_profile", NULL);

    //Absorptions
    if(absorptionCheckbox->isChecked())
    {
        qDebug() << "Absorption: True"; //verified
        addElement(doc, simulationsElement,"absorbing", "True");
    }
    else
    {
        qDebug() << "Absorption: False"; //verified
        addElement(doc, simulationsElement, "absorbing", "False");
    }

    //Tower tops
    if(towerTopsCheckbox->isChecked())
    {
        qDebug() << "Tower Tops: True"; //verified
        addElement(doc, simulationsElement, "tower_tops", "True");
    }
    else
    {
        qDebug() << "Tower Tops: False"; //verified
        addElement(doc, simulationsElement, "tower_tops", "False");
    }

    //Trapping
    if(trappingCheckbox->isChecked())
    {
        qDebug() << "Trapping: True"; //verified
        addElement(doc, simulationsElement, "trapping", "True");
    }
    else
    {
        qDebug() << "Trapping: False"; //verified
        addElement(doc, simulationsElement, "trapping", "False");
    }

    QDomElement towerElement = addElement(doc, simulationsElement, "tower", NULL);

    //Tower Shape
    qDebug() << "Selected Shape: " + shapeComboBox->itemText(shapeComboBox->currentIndex());
    addElement(doc, towerElement, "shape", shapeComboBox->itemText(shapeComboBox->currentIndex()));

    //Tower Pitch
    QString towerPitchString = towerPitchEdit->text();
    addElement(doc, towerElement, "pitch", towerPitchString);

    //Tower Width
    QString towerWidthString = towerWidthEdit->text();
    addElement(doc, towerElement, "width", towerWidthString);

    //Tower Height
    QString towerHeightString = towerHeightEdit->text();
    addElement(doc, towerElement, "height", towerHeightString);


    ///////////////////////////////////////////Output Settings/////////////////////////////////////////////////////////////////////

    QString graphsList = "";

    //Output Tab
    QDomElement outputSettingsElement = addElement(doc, simulationsElement, "output_settings",NULL);
    QDomElement graphSettingsElement = addElement(doc, outputSettingsElement, "graph_settings", NULL);
    QDomElement includePathsElement = addElement(doc, outputSettingsElement, "include_paths", NULL);

    //MaxPointPowerVsZenithAngle
    if(maxPointPowerVsZenithAngleCheckbox->isChecked())
    {
        qDebug() << "MaxPointPowerVsZenithAngle: True"; //verified
        graphsList += "MaxPointPowerVsZenithAngle, \n";
    }

    //AverageReflectionsVsAzumithal
    if(AverageReflectionsVsAzumithalCheckbox->isChecked())
    {
        qDebug() << "AverageReflectionsVsAzumithal: True"; //verified
        graphsList += "AverageReflectionsVsAzumithal, \n";
    }

    //AbsorptionEfficiencyVsAzumithal
    if(AbsorptionEfficiencyVsAzumithalCheckbox->isChecked())
    {
        qDebug() << "AbsorptionEfficiencyVsAzumithal: True"; //verified
        graphsList += "AbsorptionEfficiencyVsAzumithal,\n";
    }

    //AspectRatioVsAverageReflections
    if(AspectRatioVsAverageReflectionsCheckbox->isChecked())
    {
        qDebug() << "AspectRatioVsAverageReflections: True"; //verified
        graphsList += "AspectRatioVsAverageReflections,\n";
    }

    //IntegratedAreaRatioVsAvgNumReflections
    if(IntegratedAreaRatioVsAvgNumReflectionsCheckbox->isChecked())
    {
        qDebug() << "IntegratedAreaRatioVsAvgNumReflections: True"; //verified
        graphsList += "IntegratedAreaRatioVsAvgNumReflections,\n";
    }

    //PowerRatio3DVsAbsorbance
    if(PowerRatio3DVsAbsorbanceCheckbox->isChecked())
    {
        qDebug() << "PowerRatio3DVsAbsorbance: True"; //verified
        graphsList += "PowerRatio3DVsAbsorbance,\n";
    }

    //AvgInteractionsVsTowerSpacingLog
    if(AvgInteractionsVsTowerSpacingLogCheckbox->isChecked())
    {
        qDebug() << "AvgInteractionsVsTowerSpacingLog: True"; //verified
        graphsList += "AvgInteractionsVsTowerSpacingLog,\n";
    }

    //AvgReflectionsVsTowerHeight
    if(AvgReflectionsVsTowerHeightCheckbox->isChecked())
    {
        qDebug() << "AvgReflectionsVsTowerHeight: True"; //verified
        graphsList += "AvgReflectionsVsTowerHeight\n";
    }

    if(includePathsCheckbox->isChecked())
    {
        addElement(doc, includePathsElement, "true");
    }

    addElement(doc, graphSettingsElement, graphsList);

    ///////////////////////////////////////////END Output Settings/////////////////////////////////////////////////////////////////

    qDebug() << "XML Contents:";
    qDebug() << doc.toString();

    qDebug() << "Graphs List:";
    qDebug() << graphsList;

    //TODO: Remove this later
    if(checked)
    {
        qDebug() << "message, Pressed the damn button";
    }
}

/* Helper function to generate a DOM Element for the given DOM document
   and append it to the children of the given node. */
QDomElement InputPage::addElement( QDomDocument &doc, QDomNode &node,
                        const QString &tag,
                        const QString &value)
{
  QDomElement el = doc.createElement( tag );
  node.appendChild( el );
  if ( !value.isNull() ) {
    QDomText txt = doc.createTextNode( value );
    el.appendChild( txt );
  }
  return el;
}

void InputPage::on_addSimulationButton_clicked()
{
    qDebug() << "Clicked the Add Simulation button";

    //Create a new simulation dom element

    //Add that dom element to the existing dom structure
}

bool InputPage::validateFormInput()
{
    qDebug() << "Validating Form Input";

    //Make sure that each input is within specified range.

    return true;
}

void InputPage::on_doneButton_clicked()
{
    qDebug() << "Clicked the Done button";
}

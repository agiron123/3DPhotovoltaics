3D Photovoltaic Simulation
Version 1.3 
Last edited: 03/16/14

===================================
  Overview
===================================

 -- This program allows the user to run simulations of 3D photovoltaic cells. The user is able to configure settings for one or more simulations by using an XML file. 
 After the user has configured the XML file, they can then run the simulation using those settings and generate graphs and output files based on the results of the simulations.

===================================
  Installation Instructions
===================================

 1)  In order to run our application you will first need to install the python programming language as well as several third party packages which our application is dependent on. To install python please follow the directions at http://www.python.org/downloads/ .

 2) After you have installed python you will need to install both numpy and matplotlib from the scipy group of packages. They will need to be installed with the same version of python you intend to use when running the simulation. SciPy has very detailed instruction on how to perform installation, including common problems. These can be found at http://www.scipy.org/install.html. Specific windows installers for easy installation with Mircosoft windows can also be found at http://www.lfd.uci.edu/~gohlke/pythonlibs/.

 NOTE: If you have multiple versions of python on your machine make sure you install these dependencies so they can be used by the version of python which you intend to run our program with. 
 3) After python and all dependent packages have been installed you can get our code from github by either checking out the repo or downloading a zip at https://github.com/agiron123/3DPhotovoltaics .

===================================
  How to Run
===================================

------------------------------
  Simulation Settings
------------------------------

If you have not configured this program before, we highly recommend that you look at the file format outlined in the Appendix.
 Note that this is a copy of the file template.xml. template.xml can be copied and used as a template when configuring the simulation.
  You should only have to perform minimal changes when using this template.
The template.xml file provides comments which specify the parameter and any other applicable information.

To create a new XML configuration file just make a copy of template.xml .
 Enter any desired changes and save the file as follows: <filename>.xml where filename is a filename of your choice that is different from template.xml.
After you have saved the file, navigate to the directory in which the 3DPhotovoltaics program is located and copy the file into the directory.
You can place the file anywhere as long as you specify the correct file path relative to Main.py when running the program.

------------------------------
  Running the Program:
------------------------------

1) Using the Command Prompt or terminal, navigate to the directory where the 3DPhotovoltaics program is located.

     - Run the following command in terminal:

         python Main.py

2) You will now be asked for the location of an xml file.


3) After the prompt appears, type the file path of the xml file you wish to use for configuration. If the file is in the same directory as Main.py you can just type its name.

         name-of-file.xml

   In the event that any syntax errors in the xml file exist, the program will notify the you of the specific errors.
    You should be told exactly what is wrong and what tags need to be fixed. You will now have the option to correct these errors.

   Your simulation should now run assuming there are no syntax errors in the XML file. If it does not run, refer to the troubleshooting section at the end of the file.

===================================
  Data Output
===================================

------------------------------
  Files Types:
------------------------------

    - .csv
    - .png (For graphs)
    
------------------------------
  General Information:
------------------------------

    - All of the data for this program will be saved in a folder called “Simulation_Data” which is located in the same directory as the python script. Inside of the “Simulation_Data” folder you will see several sub-folders. These folders contain the data for the program and each type of graph. 

------------------------------
  Graph Data:
------------------------------

    - Contains:
      * .csv files
      * .png files

    - .csv files and .png files for each type of graph will be stored in a folder named after the graph it represents (eg. “Average_Number_of Reflections_vs_Azimuthal_Angle”). 

------------------------------
  Raw Data:
------------------------------

    - Contains:
      * .csv files

    - There will also be a folder called “Raw_Data.” This folder will contain all of the simulation .csv files created by the program. This folder will not contain the .csv files and .png files for graphs.

------------------------------
  Most Recent Run:
------------------------------

    - Contains:
      * .csv files
      * .png files

    - “Most_Recent_Run” is a folder that will contain the .csv files of each simulation, the .csv files for each graph, and the .png files for each graph generated in the latest run of the program. These files will be deleted and replaced after each run. It provides a quicker way to access the data from the last run.

------------------------------
  Simulation CSV File Format:
------------------------------

    - Contains:
      * Tower Information
      * Compiled Data
      * Photon (Stat) Data

    - This .csv file will contain all of the data from each simulation. It will first list the tower’s information, then the compiled data for the simulation, and finally all of the data for each photon.

    - Each file will be uniquely named by including a timestamp. (eg. “Raw_Simulation_Data_2014-03-15_01:21:05”)
    
    - An example output file is located in the Appendix under “Example Raw Data CSV Output”

------------------------------
  Graph CSV File Output:
------------------------------

    - Contains:
      * Graph Name
      * Axis Labels
      * Graph Values

    - This .csv file will contain all of the data needed to create a graph. It will first list the graph’s name, then its axis labels, and finally the data to be plotted on the graph.

    - Each file will be uniquely named by including a timestamp. (eg. “Avg_Reflections_vs_Tower_Height_2014-03-15_01:21:05.csv”, Avg_Reflections_vs_Tower_Height_2014-03-15_01:21:06.png”)

    - Example .csv Output:

Average Number of Reflections vs Azimuthal Angle
Azimuthal Angle (Degrees),Average Number of Reflections
40.0,8
50.0,5
60.0,5
...

===================================
  Troubleshooting:
===================================

--------------------------------
  Program Cannot Find XML File:
--------------------------------

    1) First be sure the file is saved at the file path you are providing to the program
    2) Then confirm that you have typed it in the correct file path when running the program.

-------------------------------
  Program Will Not Run
-------------------------------

Confirm that the XML is properly formatted. The validator should let you know of any errors and the specific details associated with them.
You can always refer to template.xml if you are unsure how something should be formated.

------------------------------
  Locating Outputted Files:
------------------------------

    1) All output files will be saved in a folder called “Simulation Data.” This folder will be located in the same directory as the python script. 
    2) Once you locate “Simulation Data,” open the folder and you will see subfolders. The names of these folders correspond to the data they store.

===================================
  Appendix:
===================================

--------------------------------
  xml_validator.xml:
--------------------------------

<?xml version="1.0" ?>
<!-- XML file to test the XML input parser. Note that this does not contain real values that are going to be used in a simulaiton. -->
<configurations>
<simulation datatype="NA"><!-- Contains settings for a single simulation. -->
<absorbing datatype="bool"></absorbing> <!-- Whether or not the simulation should model absorptions -->
<tower_tops datatype="bool"></tower_tops><!--Whether the simulation should model the photons which strike the tops of the towers or ignore them -->
<trapping datatype="bool"></trapping><!-- Whether the simulation should model photons becoming trapped -->


<material_profile datatype="NA"><!-- Information on Material used for the simulation -->
<band_gap datatype="float" range="0.0 - 9.0"></band_gap><!-- The band gap for the material in electron volts (eV) -->
<absorption_coefficient datatype="float" range="10 - 10e7"></absorption_coefficient><!-- The absorption coefficient for the material in (cm^-1) -->
</material_profile>


<tower datatype="NA"><!-- The tower for the simulation, all tower units are in micro meters -->
	<shape datatype="str" valid_set="rect_prism, cylinder, convex_polygon, ytrench, xtrench, box">
    </shape><!-- Shape of the tower. Shape must be chosen from the valid set-->
	<pitch datatype="float" range="0 - inf"></pitch><!-- Pitch of the tower. How far the towers are separated -->
	<width datatype="float" range="0 - inf"></width><!-- Width of the tower. -->
	<height datatype="float" range="0 - inf"></height><!-- Height of the tower. -->
</tower>

<!-- Note only one child from the childset may be present
 meaning that you must chose either a RealOrbit or a SimpleOrbit but cannot have both
 -->
<orbital_properties datatype="NA" child_set="real_orbit, fixed_orbit"><!-- Settings for the Orbital Properties of the simulation. -->


<real_orbit datatype="NA"><!-- Contains all the information for a real orbit representing the ISS traveling through space,
                                Currently in the process of implementation and not supported-->

<tle datatype="NA"> <!-- Contains each line for a TLE -->
<line1 datatype="str"><!-- First line of the TLE -->
</line1>
<line2 datatype="str"><!-- Second line of the TLE-->
</line2>
</tle>

<beta_angle datatype="float" range="0.0 - 360.0"></beta_angle><!-- Beta angle for the simulation in degrees -->
<interval datatype="float" range="0.0 - inf"></interval><!-- How many orbits the simulation should be run for. -->
<earthshine datatype="bool"></earthshine><!-- Whether or not Earthshine should be modeled in the simulation. -->
</real_orbit>


<fixed_orbit><!-- Contains all of the information for a orbit in which nothing is moving and the sun is a fixed point source -->
    <zenith_angle datatype="float" range="0.0 - 360.0"></zenith_angle> <!-- Zenith Angle in degrees for point source sun -->
    <azimuth_angle datatype="float" range="0.0 - 360.0"></azimuth_angle> <!-- Azimuth Angle in degrees for the point source sun -->
    <photon_count datatype="int" range="0 - inf"></photon_count> <!-- Number of photons to run the simulation for -->
</fixed_orbit>


</orbital_properties>

<non_specular_reflection datatype="bool"></non_specular_reflection><!-- Whether or not Non Specular Reflection should be accounted for in the simulation. -->
<optical_material datatype="str"></optical_material><!-- Optical materials currently not supported. Should be left blank for now -->

<output_settings datatype="NA"><!-- Lists specifying what forms of data should be outputted -->

<include_path datatype="bool"></include_path><!-- Whether to include photon paths in the CSV output files-->
<graph_settings datatype="str" list="true" valid_set="
    MaxPofloatPowerVsZenithAngle,
	AverageReflectionsVsAzumithal,
	AbsorptionEfficiencyVsAzumithal,
	AspectRatioVsAverageReflections,
	IntegratedAreaRatioVsAvgNumReflections,
	PowerRatio3DVsAbsorbance,
	AvgInteractionsVsTowerSpacingLog,
	AvgReflectionsVsTowerHeight"><!-- List of which graphs to include, names must be chosen from the valid set -->
    <!-- Currently only 	AspectRatioVsAverageReflections
	                        AvgInteractionsVsTowerSpacingLog
	                        AvgReflectionsVsTowerHeight
	    are supported -->
</graph_settings>
</output_settings>
</simulation>
</configurations>

--------------------------------
Example Raw Data CSV Output:
--------------------------------

Tower Data
height(um),width(um),shape,log_pitch,pitch(um),aspect_ratio
40.0,10.0,square,3.688879454,40.0,0.25
Compiled Data
total_number_interactions,avg_number_interactions,avg_number_reflections,total_absorbed,number_photons,total_trapped,total_number_reflections
597.0,5.97,5.49,55,100,48,549.0
Stats
zenith(degrees),interactions,wavelength,trapped,absorbed,reflections,azimuth(degrees)
85.0,3.0,21.0,False,True,9.0,35.0
…

--------------------------------



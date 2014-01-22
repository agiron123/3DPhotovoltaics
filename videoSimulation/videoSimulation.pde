// Original Author: Christian BOTKIN, created on December 2, 2013, version:12/5/13

/****************************view variables*********************************************************/
float rx=0.01*TWO_PI, ry=-0.04*TWO_PI;
int zoom = 50;
int width = 600, height = 600;
boolean light = true;
//PImage myFace;
String title ="3D Photovoltaic Cell Simulation", name ="Christian Botkin";
/*****************************data counters**********************************************************/
int photonsGenerated = 0;
int escapedNo[], absorbedNo[], interactions[], azimuth, zenith = 90+45;
/*****************************visualization variables************************************************/
pt[] displayedPos;
vec[] displayedVelocity;
float time[], deltaT[], tepsilon = 0.001, deltaDistance = 0.01;
int displayNo = 100;
/*****************************simulation variables***************************************************/
photon[] photons;
int photonNo = 1000, photonsPerAzimuth = 10000;
boolean inProgress = false, graphicsOn = true, ignoreTowerTopPhotons = false, printInteractions = true, printAbsorption = false;
float aspectRatio = 2;
float towerWidth = 1/aspectRatio;
float integratedAreaRatio = 1; 
float simulationWidth = sqrt(towerWidth*towerWidth*(integratedAreaRatio+1));
float simulationHeight = 1;

void setup() {
  //initialize view variables
  //myFace = loadImage("data/pic.jpg");
  size(width, height, P3D);
  
  //initialize visualization variables
  displayedPos = new pt[photonNo];
  displayedVelocity = new vec[photonNo];
  time = new float[photonNo];
  deltaT = new float[photonNo];
  
  //initialize simulation variables
  photons = new photon[photonNo];
  
  //initialize data counters
  escapedNo = new int[100];
  absorbedNo = new int[100];
  interactions = new int[100];
}

void draw() {
  if (ignoreTowerTopPhotons) { tepsilon = 0; } else { epsilon = 0.001; } 
  pvc cell = PVC(towerWidth, simulationWidth, simulationHeight, CZTS());
  
  if (graphicsOn) { // Visualization & Simulation fork
    background(255); // clear the screen
    pushMatrix();
    
      // orient the view properly
      translate(width/2,height/2,0);
      scale(zoom);
      if(light) lights();
      rotateX(rx); rotateY(ry); 
      rotateX(PI/2);
      
      stroke(0); strokeWeight(1);  fill(pvcMaterialColor); show(cell); // draw the photovoltaic cell
      
      if (inProgress) for(int i = 0; i < photonNo; i++) { // iterate through photons if simulation is "On"
        if (photons[i] == null) { generatePhoton(i); } // generate new photon if free space available
        if (i >= displayNo || time[i] == 0.0 || time[i] >= 1.0) { // perform simulation calculations and update display variables
          
          // acquire previous path segment data
          displayedPos[i] = copy(photons[i].P);
          displayedVelocity[i] = copy(photons[i].V);
          
          // perform simulation calculations
          hit next = calcNextHit(photons[i], cell); // calculate the next collision site
          if(next == null) { destroyPhoton(i); escapedNo[azimuth]++; continue;} // destroy/delete photon if it escaped
          if(absorb(next.w.m,photons[i])) { destroyPhoton(i); absorbedNo[azimuth]++; continue;} // destory/delete photon if it was absorbed
          photons[i].update(next); // update photon to new section of its path
          
          // update time increment variables
          deltaT[i] = deltaDistance/n(scale(next.time,displayedVelocity[i])); // time increment = distance increment / distance to be traveled (units wrong but ok)
          displayedVelocity[i] = scale(next.time,displayedVelocity[i]); // |display velocity| = distance to be traveled (units wrong but ok)
          time[i] = deltaT[i];
        } else if (i < displayNo) { // update visualization of photon
          showPath(displayedPos[i],P(displayedPos[i],time[i],displayedVelocity[i]));
          time[i] += deltaT[i];
          change = true;
        }
      }
    popMatrix();
  } else { // Simulation Only fork
    if (inProgress) for(int i = 0; i < photonNo; i++) { // iterate through photons if simulation is "On"
      if (photons[i] == null) { generatePhoton(i); } // generate new photon if free space available
      hit next = calcNextHit(photons[i], cell); // calculate the next collision site
      if (next == null) { destroyPhoton(i); escapedNo[azimuth]++; continue;} // destroy/delete photon if it escaped
      if (absorb(next.w.m,photons[i])) { destroyPhoton(i); absorbedNo[azimuth]++; continue;} // destory/delete photon if it was absorbed
      photons[i].update(next); // update photon to new section of its path
    }
  }
  
  noLights();
  if(mouseX-pmouseX != 0 || mouseY-pmouseY != 0) change = true;
  if(filming && change) {saveFrame("FRAMES/F"+nf(frameCounter++,4)+".tif");}
  fill(0); stroke(0); strokeWeight(1); displayHeader(); displayFooter(); // display HUD info/guide/menu
}
void displayHeader() { // Displays title and myFace on screen
  scribeHeader(title,0); scribeHeaderRight(name); 
  //fill(255); image(myFace, width-1.5*myFace.width/2,25,myFace.width/2,myFace.height/2); 
}
void displayFooter() { // Displays help text at the bottom
  scribeFooter("drag:rotate, z+drag:zoom, s:start/stop, g:graphics on/off, ~:toggle video (" + (filming ? "On" : "Off") + ")",2); 
  scribeFooter("-/=:decrease/increase aspect ratio, _/+:decrease/increase integrated area ratio",1);
  scribeFooter("t:switch from interactions to absorbance output (" + printAbsorption + "), f:filter out tower top photons (" + ignoreTowerTopPhotons + ")",0); 
}
void scribeHeader(String S, int i) {fill(0); text(S,10,20+i*20); noFill();} // writes black at line i
void scribeHeaderRight(String S) {fill(0); text(S,width-7.5*S.length(),20); noFill();} // writes black on screen top, right-aligned
void scribeFooter(String S, int i) {fill(0); text(S,10,height-10-i*20); noFill();} // writes black on screen at line i from bottom

void destroyPhoton(int i) {
  interactions[azimuth] += photons[i].interactions; // maintain interactions counter variable
  photons[i] = null; // destroy/delete photon
}

void generatePhoton(int i) {
  if ((absorbedNo[azimuth]+escapedNo[azimuth]) % photonsPerAzimuth == 0 && (absorbedNo[azimuth]+escapedNo[azimuth]) != 0) { // if time to update azimuth angle
    
    //print out comma sepearate values (csv) to console
    print(azimuth); // output azimuth
    if(printInteractions) { print("," + 1.0*interactions[azimuth]/(absorbedNo[azimuth]+escapedNo[azimuth])); } // output interactions if asked for
    if(printAbsorption) { print("," + (1.0*absorbedNo[azimuth]/(absorbedNo[azimuth]+escapedNo[azimuth]))); } // output interactions if asked for
    print("\n"); // end of coordinate output
    
    azimuth++; if(azimuth == 91) { inProgress = false;} // update azimuth angle
  }
  
  time[i] = 0.0; // reset time variable to start of path segment
  vec V = sphericalV(1.0, azimuth, zenith); // calculate new velocity from spherical coordinates (will change in future)
  
  // generate new photon. if ignore tower top photons is "On", only create photons Not originating above tower
  photons[i] = Photon(P(random(-simulationWidth/2,simulationWidth/2),random(-simulationWidth/2,simulationWidth/2),simulationHeight/2+tepsilon), V,random(200,827));
  while(ignoreTowerTopPhotons && photons[i].P.x >= -towerWidth/2 && photons[i].P.x <= towerWidth/2 && photons[i].P.y >= -towerWidth/2 && photons[i].P.y <= towerWidth/2) {
    photons[i] = Photon(P(random(-simulationWidth/2,simulationWidth/2),random(-simulationWidth/2,simulationWidth/2),simulationHeight/2+tepsilon), V,random(200,827));
  }
  displayedPos[i] = copy(photons[i].P); // update display position
  displayedVelocity[i] = null; // clear display velocity
}

void mouseDragged() {
  change = true;
  if (!keyPressed) { rx-=PI*(mouseY-pmouseY)/height; ry+=PI*(mouseX-pmouseX)/width;};
  if (keyPressed) {
    if (key=='z') { zoom+=mouseY-pmouseY;}
  }
}
  
void keyPressed() {
  if(key == '=' && !inProgress) { aspectRatio=aspectRatio*2; towerWidth=1/aspectRatio; simulationWidth=sqrt(towerWidth*towerWidth*(integratedAreaRatio+1)); }
  if(key == '-' && !inProgress) { aspectRatio=aspectRatio/2; towerWidth=1/aspectRatio; simulationWidth=sqrt(towerWidth*towerWidth*(integratedAreaRatio+1)); }
  if(key == '+' && !inProgress) { integratedAreaRatio=integratedAreaRatio*2; simulationWidth=sqrt(towerWidth*towerWidth*(integratedAreaRatio+1)); }
  if(key == '_' && !inProgress) { integratedAreaRatio=integratedAreaRatio/2; simulationWidth=sqrt(towerWidth*towerWidth*(integratedAreaRatio+1)); }
  if(key == 't' && !inProgress) { printInteractions = !printInteractions; printAbsorption = !printAbsorption; }
  if(key == 'f' && !inProgress) { ignoreTowerTopPhotons = !ignoreTowerTopPhotons; }
  if(key == 's' && !inProgress) { inProgress = true; return;}
  if(key == 's' && inProgress) { inProgress = false; print("Photons escaped: " + escapedNo[azimuth] + "\nPhotons absorbed: " + absorbedNo[azimuth] + "\n");}
  if(key == 'g') {
    if(graphicsOn) { graphicsOn = false; frameRate(MAX_INT);}
    else { graphicsOn = true; frameRate(60);}
  }
  if(key=='~') { filming=!filming; } // filming on/off capture frames into folder FRAMES 
}
boolean filming=false;  // when true frames are captured in FRAMES for a movie
int frameCounter=0;     // count of frames captured (used for naming the image files)
boolean change=false;   // true when the user has presed a key or moved the mouse
  
//********************************************************************************************************************************************************

color pvcMaterialColor = color(0,0,255), pvcPartitionColor = color(0, 255, 0);

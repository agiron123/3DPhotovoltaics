float hc = 1239.84193; //Planck's constant times speed of light (in electron volt nanometers)

boolean absorb(material m, photon p) {
  if (m == null) {
    return false;
  } else if (m.bandGap > hc / p.wavelength) {
    return false;
  } else {
    float alpha = 10000000.0*4.0*PI*0.00658/p.wavelength; // alpha = 4*PI*k/lambda;
    float x = random(0.0001, 0.01);
    if (random(1.0) > alpha*x) {return true;} else {return false;}
  }
}

class photon { pt P; vec V; float wavelength; int interactions = 0;
  photon (pt pP, vec pV, float pWavelength) { P = pP; V = pV; wavelength = pWavelength;}
  void update(hit h) {
    if (h.w.m == null) { //if this is a boundary wall
      P = P(1.0,h.intersection,-2.0,h.w.center);
    } else {
      P = h.intersection;
      vec IN = scale(dot(V,h.w.normal),h.w.normal);
      V = add(V,scale(-2,IN));
      interactions++;
    }
  }
}
photon Photon(pt P, vec V, float wavelength) { return new photon(P,V,wavelength);}

class material { float bandGap = 0.0, absorptionC = 0.0, fourPiK;
  material () {}
  material (float mBandGap, float mAbsorptionC) { bandGap = mBandGap; absorptionC = mAbsorptionC;}
}
material CZTS() { return new material(1.45,0.0001);}

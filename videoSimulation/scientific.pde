float hc = 1239.84193; //Planck's constant times speed of light (in electron volt nanometers)

//@Walker, ported over to python need confirmation with Ricardo and Christian of correctness
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
  //@Walker seems here that boundary wrapping logic is contained within photon update, we are checking for this in simulation now
  //maybe add a wrap_around method to photon so it can wrap itself around after simulation has modified the control flow
  void update(hit h) {
    if (h.w.m == null) { //if this is a boundary wall
      P = P(1.0,h.intersection,-2.0,h.w.center);
    } else {
      P = h.intersection;
      vec IN = scale(dot(V,h.w.normal),h.w.normal);
      V = add(V,scale(-2,IN));
      //@Walker, this would be very similar if photon had a reference to stat, need to discuss benefits/drawbacks of this reference
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

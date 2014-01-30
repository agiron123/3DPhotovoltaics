float epsilon = 0.000001;

void show(wall W) { beginShape(); v(W.A); v(W.B); v(W.C); v(W.D); endShape(CLOSE);}
void show(pvc cell) {
  show(cell.w1); show(cell.w2); show(cell.w3); show(cell.w4); show(cell.wtop); show(cell.wfloor);
  noFill(); show(cell.b1); show(cell.b2); show(cell.b3); show(cell.b4);
}
void showNormal(pvc cell) {
  strokeWeight(10); stroke(255,0,0); 
  showNormal(cell.w1); showNormal(cell.w2); showNormal(cell.w3); showNormal(cell.w4); showNormal(cell.wtop); showNormal(cell.wfloor);
  showNormal(cell.b1); showNormal(cell.b2); showNormal(cell.b3); showNormal(cell.b4);
}
void showNormal(wall w) {
  show(center(w),scale(0.25,w.normal));
}

class wall { pt A, B, C, D, center; material m; vec normal;
  wall () {}
  wall (pt wA, pt wB, pt wC, pt wD) { A = wA; B = wB; C = wC; D = wD; center = P(wA,wB,wC,wD); normal = normalize(cross(V(wA,wB),V(wA,wC)));}
  wall (pt wA, pt wB, pt wC, pt wD, material wm) { A = wA; B = wB; C = wC; D = wD; m = wm; center = P(wA,wB,wC,wD); normal = normalize(cross(V(wA,wB),V(wA,wC)));}
}
wall W(pt A, pt B, pt C, pt D) { return new wall(A,B,C,D);}
wall W(pt A, pt B, pt C, pt D, material m) { return new wall(A,B,C,D,m);}
pt center(wall w) { return P(w.A,w.B,w.C,w.D);}

class hit { wall w; photon p; float time; pt intersection;
  hit () {}
  hit (wall hw, photon wp) {
    w = hw; p = wp;
    time = intersectionT(p, w);
    intersection = P(p.P,time,p.V);
    //@Walker here and below concerned with determining membership within quad, should not be relevant to new design
    vec PQ = V(w.A,intersection);
    vec N = cross(V(w.A,w.B),w.normal);
    if (dot(PQ,N)>0) { time = MAX_FLOAT;}
    PQ = V(w.B,intersection);
    N = cross(V(w.B,w.C),w.normal);
    if (dot(PQ,N)>0) { time = MAX_FLOAT;}
    PQ = V(w.C,intersection);
    N = cross(V(w.C,w.D),w.normal);
    if (dot(PQ,N)>0) { time = MAX_FLOAT;}
    PQ = V(w.D,intersection);
    N = cross(V(w.D,w.A),w.normal);
    if (dot(PQ,N)>0) { time = MAX_FLOAT;}
  }
}

hit calcNextHit(photon p, pvc cell) {
  hit closest = null;
  float closestTime = MAX_FLOAT;
  hit next = new hit(cell.w1, p); if (next.time < closestTime && next.time > epsilon) { closest = next; closestTime = next.time;}
  next = new hit(cell.w2, p); if (next.time < closestTime && next.time > epsilon) { closest = next; closestTime = next.time;}
  next = new hit(cell.w3, p); if (next.time < closestTime && next.time > epsilon) { closest = next; closestTime = next.time;}
  next = new hit(cell.w4, p); if (next.time < closestTime && next.time > epsilon) { closest = next; closestTime = next.time;}
  next = new hit(cell.b1, p); if (next.time < closestTime && next.time > epsilon) { closest = next; closestTime = next.time;}
  next = new hit(cell.b2, p); if (next.time < closestTime && next.time > epsilon) { closest = next; closestTime = next.time;}
  next = new hit(cell.b3, p); if (next.time < closestTime && next.time > epsilon) { closest = next; closestTime = next.time;}
  next = new hit(cell.b4, p); if (next.time < closestTime && next.time > epsilon) { closest = next; closestTime = next.time;}
  next = new hit(cell.wtop, p); if (next.time < closestTime && next.time > epsilon) { closest = next; closestTime = next.time;}
  next = new hit(cell.wfloor, p); if (next.time < closestTime && next.time > epsilon) { closest = next; closestTime = next.time;}
  if (closestTime == MAX_FLOAT) {return null;}
  return closest;
}
float intersectionT(photon p, wall w) {
  float t = -dot(V(w.A,p.P),w.normal)/dot(p.V,w.normal);
  return t;
}
//@Walker, what are b1,b2,b3,b4?
class pvc { wall w1, w2, w3, w4, wfloor, wtop, b1, b2, b3, b4;
  pvc () {}
  pvc (wall pvcw1, wall pvcw2, wall pvcw3, wall pvcw4) { w1 = pvcw1; w2 = pvcw2; w3 = pvcw3; w4 = pvcw4; }
  pvc (float tWidth, float sWidth, float sHeight, material m) {
    pt A = P(-sWidth/2,-sWidth/2,-sHeight/2);
    pt B = P( sWidth/2,-sWidth/2,-sHeight/2);
    pt C = P( sWidth/2, sWidth/2,-sHeight/2);
    pt D = P(-sWidth/2, sWidth/2,-sHeight/2);
    wfloor = W(A,B,C,D,m);
    A = P( tWidth/2,-tWidth/2,-sHeight/2);
    B = P( tWidth/2,-tWidth/2, sHeight/2);
    C = P(-tWidth/2,-tWidth/2, sHeight/2);
    D = P(-tWidth/2,-tWidth/2,-sHeight/2);
    w1 = W(A,B,C,D,m);
    A = P(-tWidth/2,-tWidth/2,-sHeight/2);
    B = P(-tWidth/2,-tWidth/2, sHeight/2);
    C = P(-tWidth/2, tWidth/2, sHeight/2);
    D = P(-tWidth/2, tWidth/2,-sHeight/2);
    w2 = W(A,B,C,D,m);
    A = P( tWidth/2, tWidth/2,-sHeight/2);
    B = P( tWidth/2, tWidth/2, sHeight/2);
    C = P( tWidth/2,-tWidth/2, sHeight/2);
    D = P( tWidth/2,-tWidth/2,-sHeight/2);
    w3 = W(A,B,C,D,m);
    A = P(-tWidth/2, tWidth/2,-sHeight/2);
    B = P(-tWidth/2, tWidth/2, sHeight/2);
    C = P( tWidth/2, tWidth/2, sHeight/2);
    D = P( tWidth/2, tWidth/2,-sHeight/2);
    w4 = W(A,B,C,D,m);
    A = P(-tWidth/2,-tWidth/2, sHeight/2);
    B = P( tWidth/2,-tWidth/2, sHeight/2);
    C = P( tWidth/2, tWidth/2, sHeight/2);
    D = P(-tWidth/2, tWidth/2, sHeight/2);
    wtop = W(A,B,C,D,m);
    A = P(-sWidth/2,-sWidth/2,-sHeight/2);
    B = P(-sWidth/2,-sWidth/2, sHeight/2);
    C = P( sWidth/2,-sWidth/2, sHeight/2);
    D = P( sWidth/2,-sWidth/2,-sHeight/2);
    b1 = W(A,B,C,D);
    A = P(-sWidth/2, sWidth/2,-sHeight/2);
    B = P(-sWidth/2, sWidth/2, sHeight/2);
    C = P(-sWidth/2,-sWidth/2, sHeight/2);
    D = P(-sWidth/2,-sWidth/2,-sHeight/2);
    b2 = W(A,B,C,D);
    A = P( sWidth/2,-sWidth/2,-sHeight/2);
    B = P( sWidth/2,-sWidth/2, sHeight/2);
    C = P( sWidth/2, sWidth/2, sHeight/2);
    D = P( sWidth/2, sWidth/2,-sHeight/2);
    b3 = W(A,B,C,D);
    A = P( sWidth/2, sWidth/2,-sHeight/2);
    B = P( sWidth/2, sWidth/2, sHeight/2);
    C = P(-sWidth/2, sWidth/2, sHeight/2);
    D = P(-sWidth/2, sWidth/2,-sHeight/2);
    b4 = W(A,B,C,D);
  }
}
pvc PVC(float pvctWidth, float pvcsWidth, float pvcsHeight, material pvcm) { return new pvc(pvctWidth,pvcsWidth,pvcsHeight,pvcm);}

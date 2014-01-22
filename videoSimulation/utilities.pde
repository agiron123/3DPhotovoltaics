class pt { float x = 0.0, y = 0.0, z = 0.0;
  pt () {}
  pt (float px, float py, float pz) { x = px; y = py; z = pz;}
}
pt P(float x, float y, float z) { return new pt(x,y,z); }
pt P(pt P, float c, vec V) { return P(P.x+c*V.dx, P.y+c*V.dy, P.z+c*V.dz);}
pt P(pt P, vec V) { return P(P.x+V.dx, P.y+V.dy, P.z+V.dz);}
pt P(float a, pt A, float b, pt B) { return P(a*A.x+b*B.x,a*A.y+b*B.y,a*A.z+b*B.z);}
pt P(pt A, pt B, pt C, pt D) { return P((A.x+B.x+C.x+D.x)/4,(A.y+B.y+C.y+D.y)/4,(A.z+B.z+C.z+D.z)/4);}
pt copy(pt P) { return P(P.x,P.y,P.z);}
float d(pt A, pt B) { return n(V(A,B));}

class vec { float dx = 0.0, dy = 0.0, dz = 0.0;
  vec () {}
  vec (float vx, float vy, float vz) { dx = vx; dy = vy; dz = vz;}
}
vec V(float dx, float dy, float dz) { return new vec(dx,dy,dz); }
vec V(pt A, pt B) { return V(B.x-A.x,B.y-A.y,B.z-A.z);}
vec sphericalV(float rho, float azimuth, float zenith) {
  zenith *= PI/180;
  azimuth *= PI/180;
  return V(rho*sin(zenith)*cos(azimuth),rho*sin(zenith)*sin(azimuth),rho*cos(zenith));
}
vec cross(vec A, vec B) { return V(A.dy*B.dz-A.dz*B.dy, -A.dx*B.dz+A.dz*B.dx, A.dx*B.dy-A.dy*B.dx); }
float dot(vec A, vec B) { return A.dx*B.dx + A.dy*B.dy + A.dz*B.dz;}
vec add(vec A, vec B) { return V(A.dx+B.dx,A.dy+B.dy,A.dz+B.dz);}
vec normalize(vec V) { float norm = n(V); return V(V.dx/norm, V.dy/norm, V.dz/norm);}
vec subtract(vec A, vec B) { return V(A.dx-B.dx, A.dy-B.dy, A.dz-B.dz);}
vec scale(float c, vec V) { return V(c*V.dx, c*V.dy, c*V.dz);}
float angle(vec A, vec B) { return acos(dot(A,B)/n(A)/n(B));}
float n(vec V) { return sqrt(dot(V, V));}
vec copy(vec V) { return V(V.dx,V.dy,V.dz);}

void show(pt A, pt B, pt C, pt D) { beginShape(); v(A); v(B); v(C); v(D); endShape(CLOSE);}
void show(pt A, pt B) { line(A.x,A.y,A.z,B.x,B.y,B.z);}
void show(pt A, float t, pt B) { line(A.x,A.y,A.z,A.x-t*A.x+t*B.x,A.y-t*A.y+t*B.y,A.z-t*A.z+t*B.z);}
void show(pt P, vec V) { show(P,P(P,V));}
void v(pt P) { vertex(P.x,P.y,P.z);}
 
void showPath(pt P, pt Q) {
  vec N = cross(V(0,0,1),V(P,Q));
  fill(255,255,0); noStroke(); pushMatrix(); translate(P.x,P.y,P.z); rotate(angle(V(0,0,1),V(P,Q)),N.dx,N.dy,N.dz); showStub(d(P,Q),0.005); popMatrix();
}
void showFan(float d, float r) {
  float da = TWO_PI/36;
  beginShape(TRIANGLE_FAN);
    vertex(0,0,d);
    for(float a=0; a<=TWO_PI+da; a+=da) vertex(r*cos(a),r*sin(a),0);
  endShape(CLOSE);
}
void showCollar(float d, float r, float rd) {
  float da = TWO_PI/36;
  beginShape(QUAD_STRIP);
    for(float a=0; a<=TWO_PI+da; a+=da) {vertex(r*cos(a),r*sin(a),0); vertex(rd*cos(a),rd*sin(a),d);}
  endShape(CLOSE);
}
void showCone(float d, float r) {showFan(d,r);  showFan(0,r);}
void showStub(float d, float r) {
  showCollar(d,r,r); showFan(0,r);  pushMatrix(); translate(0,0,d); showFan(0,r); popMatrix();
}

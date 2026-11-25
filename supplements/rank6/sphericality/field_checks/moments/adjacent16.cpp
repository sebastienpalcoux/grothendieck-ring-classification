#include <algorithm>
#include <array>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
using LL=long long;
using L=__int128;
const LL S=1000000000LL;
LL fl(L p,L q){assert(q); if(q<0)return fl(-p,-q);return p>=0 ? LL(p/q) : -LL((-p+q-1)/q);}
LL ce(L p,L q){return -fl(-p,q);}
struct I{LL l,h; I(LL a,LL b): l(a),h(b){} I(int a):l(a*S),h(a*S){} };
I operator+(I a,I b){return I(a.l+b.l,a.h+b.h);}
I operator-(I a,I b){return I(a.l-b.h,a.h-b.l);}
I operator*(I a,I b){auto v={L(a.l)*b.l,L(a.l)*b.h,L(a.h)*b.l,L(a.h)*b.h};return I(fl(*std::min_element(v.begin(),v.end()),S),ce(*std::max_element(v.begin(),v.end()),S));}
I operator/(I a,I b){assert(b.l>0);return a*I(fl(L(S)*S,b.h),ce(L(S)*S,b.l));}
I cap(I a,I b){return I(std::max(a.l,b.l),std::min(a.h,b.h));}
bool bad(I a){return a.l>a.h;}
I sq(I a){if(a.l>=0||a.h<=0)return a*a;return I(0,std::max((I(a.l,a.l)*I(a.l,a.l)).h,(I(a.h,a.h)*I(a.h,a.h)).h));}
I ab(I a){if(a.l>=0)return a;if(a.h<=0)return I(0)-a;return I(0,std::max(-a.l,a.h));}
LL root(LL a){assert(a>=0);LL t=std::sqrt((long double)a*S);while(L(t)*t>L(a)*S)--t;while(L(t+1)*(t+1)<=L(a)*S)++t;return t;}
I sqrtI(I a){return I(root(a.l),root(a.h)+1);}
const I zero=I(0),one=I(1),unit=I(0,S),e=I(0,4000),gg=I(2828427124LL,2828427125LL);
bool even_reject(I Q,I z,I v,I U, I &r,I &B,I &b,I &w0,I &C0){
 r=cap(unit,U*(one-Q-e)/(Q+U*e));if(bad(r))return true;
 B=cap(I(S/25,24*S/25),one-Q-e*(one+r));if(bad(B))return true;
 b=v/Q; w0=one-z-v; I w=cap(I(S/5,S),w0-r*e*unit);if(bad(w))return true;
 auto F=[&](I a,I p0){
  return (I(8)*sq(I(2)*(p0+v)-one)+I(2)*gg*ab(I(2)*(e*r+Q)-one)).l>8*S
   ||(I(16)*(sq(p0-v)+sq(z-w))+I(8)*sqrtI(sq(e*r-Q)+sq(e-B))).l>8*S;
 }; if(F(unit,e*unit))return true;
 C0=B-Q*e*r/B;
 return false;
}
bool survives(I Q,I z,I v,I U){
 I r(0),B(0),b(0),w0(0),C0(0);
 if(even_reject(Q,z,v,U,r,B,b,w0,C0))return false;
 I base=r*z+e*b+Q*w0/B;
 I allA=cap(unit,I(0,b.h)); 
 for(LL h=std::max<LL>(1,ce(base.l,S)|1);h*S<=(base+allA*C0).h;h+=2){
  I a=cap(allA,(I((int)h)-base)/C0);
  if(bad(a))continue;
  I p0=a*r*e,w=cap(I(S/5,S),w0-p0),c=w/B;if(bad(w)||a.l>c.h)continue;
  I K=r*z*a+z*b+Q*b*c+B*c*a;
  if((std::max<LL>(1,ce(K.l,S)|1))*S>K.h)continue;
  std::array<I,4> p={p0,z,v,w},q={r*e,e,Q,B};
  bool cant=false;
  for(int s=1;s<=3;++s){
   I lhs=sq(p[s]);
   for(int k=1;k<4;++k)lhs=lhs+p0*sq(p[(k+s)%4])/p[k];
   if(lhs.h<(a*(sq(q[s])+r*sq(q[(1+s)%4]))).l)cant=true;
  }
  if(!cant)return true;
 }return false;
}
long long visits;
void check(I Q,I z,I v,I U,int depth){
 visits++;
 if(!survives(Q,z,v,U))return;
 if(depth>63){std::cout<<"OPEN "<<Q.l<<" "<<z.l<<" "<<v.l<<" "<<U.l<<" "<<U.h<<"\n";std::exit(1);}
 I *wid=&Q;
 if(z.h-z.l>wid->h-wid->l)wid=&z;
 if(v.h-v.l>wid->h-wid->l)wid=&v;
 LL m=(wid->l+wid->h)/2;I orig=*wid;
 wid->h=m;check(Q,z,v,U,depth+1);
 *wid=I(m,orig.h);check(Q,z,v,U,depth+1);
}
int main(){
 I uplus(5828427124LL,5828427125LL),umin(171572875,171572876);
 I u=uplus;
 for(int n=1;n>=-6;--n){
  if(n==0)u=one;
  if(n<0)u=u*umin;
  if(n==-6)u.l=0;
  visits=0;check(I(S/25,24*S/25),I(S/5,4*S/5),I(S/1000,2*S/5),u,0);
  std::cout<<n<<" visited "<<visits<<"\n";
 }
}

#include <cmath>
#include <cstdint>
#include <iostream>
using I=std::int64_t;
using W=__int128_t;
I isqrt(I n){I r=std::sqrt((long double)n);while((r+1)*(r+1)<=n)++r;while(r*r>n)--r;return r;}
W fourth(I n){W q=W(n)*n;return q*q;}
int main(int argc,char**argv){
 const I cap=argc==2?std::stoi(argv[1]):398;
 // x_i=floor(10^9 y^i), y=sqrt((5+sqrt5)/2). Verified separately.
 const I scale=1000000000,r=1902113032,r2=3618033988,r3=6881909602;
 I nrows=0;
 for(I c=-isqrt(cap*cap/5);c<=isqrt(cap*cap/5);++c)
 for(I d=-isqrt(cap*cap/10);d<=isqrt(cap*cap/10);++d)
 for(I b=-cap;b<=cap;++b){
  if(!b&&!d)continue;
  I e=-(b*r+c*r2+d*r3)/scale;
  for(I a=e-1;a<=e+2;++a){
   // Interval comparison for 0<physical ratio<1, includes both endpoints.
   I low=a*scale+b*r+c*r2+d*r3+std::min(I(0),b)+std::min(I(0),c)+std::min(I(0),d);
   I hi=low+std::abs(b)+std::abs(c)+std::abs(d);
   if(low>=scale||hi<=0)continue;
   I A=4*a+10*c;
   if(A<=4||A>cap)continue;
   I x=a*a-5*c*c,y=2*a*c+5*c*c;
   I s=b*b-5*d*d,t=2*b*d+5*d*d;
   I u=x+5*t,v=y-s-5*t;
   I B=2*u+5*v+4*(a*a+5*a*c+5*c*c);
   I C=2*(2*a*u+5*(a*v+c*u)+10*c*v);
   I N=u*u+5*u*v+5*v*v;
   if(B<=0||C<=0||N<=0)continue;
   if(B-3*A+6>0&&C-2*B+3*A-4>0&&N-C+B-A+1>0)continue;
   if(fourth(A)%N||fourth(B)%(W(N)*N)||fourth(C)%(W(N)*N*N))continue;
   std::cout<<a<<' '<<b<<' '<<c<<' '<<d<<' '<<A<<' '<<B<<' '<<C<<' '<<N<<'\n';++nrows;
  }
 }
 std::cerr<<nrows<<" retained representatives\n";
}

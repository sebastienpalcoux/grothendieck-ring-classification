#include <iostream>
#include <numeric>
#include <cstdlib>
using L=long long;
// Coefficient order: 1, sqrt(2), sqrt(2+sqrt(2)), sqrt(2-sqrt(2)).
int main(){
 for (L a=1;a<=80;++a)for (L b=-a;b<=a;++b)for(L c=-2*a;c<=2*a;++c)for (L d=-2*a;d<=2*a;++d){
  L h=c*c+d*d,k=c*c-d*d+2*c*d;
  L I=a*a+2*b*b-2*h, J=2*a*b-k, N=I*I-2*J*J;
  if (N!=1&&N!=2&&N!=4&&N!=8)continue;
  if (a*a<=2*b*b||I<=0)continue;
  // Only local minima need be retained; descent preserves the bound.
  // Trace(z*u) and Trace(z/u) for each positive unit (3+2sqrt2), (1+y)^2, (1+z)^2.
  if(3*a-4*std::abs(b)<a)continue;
  if(3*a+2*b+4*c<a || 5*a-6*b-4*c+8*d<a)continue;
  if(3*a-2*b+4*d<a || 5*a+6*b-8*c-4*d<a)continue;
  std::cout<<a<<' '<<b<<' '<<c<<' '<<d<<'\n';
 }
}

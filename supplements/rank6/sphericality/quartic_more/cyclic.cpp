// Exact outer enumeration in cyclic quartic presentations.
#include <cstdint>
#include <cmath>
#include <fstream>
#include <iostream>
#include <numeric>
using i64=std::int64_t;
using i128=__int128_t;
i64 isqrt(i64 n){i64 r=std::sqrt((long double)n);while((r+1)*(r+1)<=n)++r;while(r*r>n)--r;return r;}
i128 fourth(i64 n){i128 z=(i128)n*n;return z*z;}
int main(int argc,char**argv){
 if(argc!=3)return 2;
 std::ifstream input(argv[1]);std::ofstream out(argv[2]);if(!input||!out)return 2;
 i64 a,J,D,b,c,m,I,cap,fields=0,tuples=0,integral=0,tp=0,small=0,dnumbers=0;
 while(input>>a>>J>>D>>b>>c>>m>>I>>cap){
  ++fields;const i64 k=(a==D)?1:2;
  const i64 H=std::lcm((i64)4,I),H2=H*H,H3=H2*H;const i128 H4=(i128)H2*H2;
  for(i64 A=5;A<=cap;++A){
   if(A*I%4)continue;
   i64 U=isqrt((A*A-1)/a);
   for(i64 u=0;u<=U;++u){
    if(u*k*I%4)continue;
    const i64 R2=(I*I*(A*A+a*u*u)-1)/(16*m*D),V=isqrt(R2);
    for(i64 v=0;v<=V;++v){
     const i64 W=isqrt(R2-v*v),low=(u&&v)?-W:0;
     for(i64 w=low;w<=W;++w){
      if(!v&&!w)continue;
      if(!u&&!v)continue; // Rotate a nonzero axis to v>0.
      ++tuples;
      const i64 n0=A*H/4,n1=u*k*H/4,n2=v*H/I,n3=w*H/I;
      const i128 vv=(i128)n2*n2+(i128)n3*n3;
      const i128 diff=b*((i128)n2*n2-(i128)n3*n3)+2*c*(i128)n2*n3;
      const i128 Bn=6*(i128)n0*n0-2*D*(i128)n1*n1-2*m*D*vv;
      const i128 Cn=4*(i128)n0*n0*n0-4*n0*D*(i128)n1*n1-4*n0*m*D*vv+4*m*D*n1*diff;
      const i128 Un=(i128)n0*n0+D*(i128)n1*n1-m*D*vv;
      const i128 Vn=2*(i128)n0*n1-m*diff;
      const i128 Nn=Un*Un-D*Vn*Vn;
      if(Bn%H2||Cn%H3||Nn%H4)continue;
      ++integral;const i64 B=Bn/H2,C=Cn/H3,N=Nn/H4;
      if(B<=0||C<=0||N<=0)continue;
      ++tp;
      if(A-4>0&&B-3*A+6>0&&C-2*B+3*A-4>0&&N-C+B-A+1>0)continue;
      ++small;
      if(fourth(A)%N||fourth(B)%((i128)N*N)||fourth(C)%((i128)N*N*N))continue;
      ++dnumbers;
      out<<a<<' '<<J<<' '<<D<<' '<<b<<' '<<c<<' '<<m<<' '<<I<<' '<<A<<' '<<u<<' '<<v<<' '<<w<<' '<<B<<' '<<C<<' '<<N<<'\n';
     }
    }
   }
  }
 }
 std::cout<<"presentations "<<fields<<"\ncanonical_tuples "<<tuples<<"\nintegral "<<integral<<"\ntotally_positive "<<tp<<"\nminimum_below_one "<<small<<"\ndnumbers "<<dnumbers<<"\n";
}

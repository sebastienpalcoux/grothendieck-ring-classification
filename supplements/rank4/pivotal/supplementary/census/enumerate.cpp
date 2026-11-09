// Complete rank-four census with a strict, exact FP-dimension bound.
// Generic exact linear algebra and S3 representatives. No input list.
#include <algorithm>
#include <array>
#include <cmath>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>
#include "linear_box.hpp"
using I=long long;
using P=std::array<I,10>;
using T=std::array<std::array<std::array<I,4>,4>,4>;
// C=sum_i N_i N_i^T is the Casimir matrix. Its largest eigenvalue is
// FPdim(R). Thus FPdim(R)<D iff D*I-C is positive definite. Bareiss
// elimination computes its leading principal minors exactly; int128 is
// ample for our stated ranges (M<=59 and D<=3600).
bool bounded(const T&R,I D){
 using W=__int128_t;
 W Q[4][4]{};
 for(int j=0;j<4;++j)for(int k=0;k<4;++k){
  Q[j][k]=(j==k?D:0);
  for(int i=0;i<4;++i)for(int l=0;l<4;++l)Q[j][k]-=R[i][j][l]*R[i][k][l];
 }
 for(int j=0;j<4;++j)if(Q[j][j]<=0)return false;
 W previous=1;
 for(int k=0;k<4;++k){
  W pivot=Q[k][k];if(pivot<=0)return false;if(k==3)return true;
  for(int i=k+1;i<4;++i)for(int j=k+1;j<4;++j){
   W numerator=Q[i][j]*pivot-Q[i][k]*Q[k][j];
   if(numerator%previous)throw std::logic_error("Bareiss exact division");
   Q[i][j]=numerator/previous;
  }
  previous=pivot;
 }
 return false;
}
T tensor_s(const P&p){
 auto[a,b,c,d,e,f,g,h,i,j]=p;
 return T{{{{{1,0,0,0},{0,1,0,0},{0,0,1,0},{0,0,0,1}}},
 {{{0,1,0,0},{1,a,b,c},{0,b,d,e},{0,c,e,f}}},
 {{{0,0,1,0},{0,b,d,e},{1,d,g,h},{0,e,h,i}}},
 {{{0,0,0,1},{0,c,e,f},{0,e,h,i},{1,f,i,j}}}}};
}
T tensor_n(I a,I b,I c,I d,I e,I f){
 T R{{{{{1,0,0,0},{0,1,0,0},{0,0,1,0},{0,0,0,1}}},
 {{{0,1,0,0},{1,a,b,b},{0,b,c,d},{0,b,d,c}}},
 {{{0,0,1,0},{0,b,c,d},{0,d,e,f},{1,c,e,e}}},
 {{{0,0,0,1},{0,b,d,c},{1,c,e,e},{0,d,f,e}}}}};
 return R;
}
bool valid(const P&p){auto[a,b,c,d,e,f,g,h,i,j]=p;return
 a*d-b*b+b*g+c*h-d*d-e*e+1==0&&a*e-b*c+b*h+c*i-d*e-e*f==0&&
 b*e-c*d+d*h-e*g+e*i-f*h==0&&a*f+b*i-c*c+c*j-e*e-f*f+1==0&&
 b*f-c*e+d*i-e*h+e*j-f*i==0&&d*f-e*e+g*i-h*h+h*j-i*i+1==0;}
int main(int argc,char**argv){
 if(argc<3){std::cerr<<"Usage: enumerate M D [--no-early-dimension] [--no-dimension-filter]\n";return 2;}
 bool early_dimension=true,final_dimension=true;
 for(int k=3;k<argc;++k){
  std::string flag=argv[k];
  if(flag=="--no-early-dimension")early_dimension=false;
  else if(flag=="--no-dimension-filter")final_dimension=false;
  else throw std::invalid_argument("unknown census option");
 }
 I M=std::stoll(argv[1]),D=std::stoll(argv[2]);
 // These ranges keep integer products and fraction-free minors exact.
 // The arithmetic bounds are documented in census/README.md.
 if(M<1||M>59||D<5||D>3600)throw std::invalid_argument("require 1<=M<=59 and 5<=D<=3600");
 const std::array<std::array<int,3>,10> triples{{{0,0,0},{0,0,1},{0,0,2},
   {0,1,1},{0,1,2},{0,2,2},{1,1,1},{1,1,2},{1,2,2},{2,2,2}}};
 std::vector<std::array<int,10>> maps;std::array<int,3> perm{0,1,2};
 do{std::array<int,10> map{};for(int k=0;k<10;++k){
   std::array<int,3> tri{perm[triples[k][0]],perm[triples[k][1]],perm[triples[k][2]]};
   std::sort(tri.begin(),tri.end());map[k]=std::find(triples.begin(),triples.end(),tri)-triples.begin();
  }maps.push_back(map);
 }while(std::next_permutation(perm.begin(),perm.end()));
 auto emit=[&](const P&p){
  if(!valid(p)||(final_dimension&&!bounded(tensor_s(p),D)))return;
  // b is minimal among the six mixed entries. Compare only images
  // preserving this condition, not all images of the tuple.
  for(const auto&map:maps){if(p[map[1]]!=p[1])continue;
   for(int k=0;k<10;++k){if(p[map[k]]<p[k])return;if(p[map[k]]>p[k])break;}}
  std::cout<<"S";for(I v:p)std::cout<<' '<<v;std::cout<<'\n';
 };

 using W=__int128_t;

 for(I b=0;b<=M;++b)for(I c=0;c<=M;++c)for(I d=0;d<=M;++d)
 for(I e=0;e<=M;++e)for(I f=0;f<=M;++f){
  if(early_dimension&&2+2*b*b+2*c*c+d*d+2*e*e+f*f>=D)continue;
  // Unknowns are (g,h,j,i,a); rows are the first five self-dual equations.
  // Their order is changed only to simplify ordinary Gaussian pivoting.
  W A[5][6]={{b,c,0,0,d,b*b+d*d+e*e-1},
             {0,b,0,c,e,b*c+d*e+e*f},
             {0,0,c,b,f,c*c+e*e+f*f-1},
             {-e,d-f,0,e,0,c*d-b*e},
             {0,-e,e,d-f,0,c*e-b*f}};
  auto accept=[&](const I*x){
   P p{x[4],b,c,d,e,f,x[0],x[1],x[3],x[2]};
   if(b!=std::min({b,c,d,f,x[1],x[3]}))return;
   emit(p);
  };
  census::integer_box(A,M,accept);
 }
 // Direct bounded loops for a dual pair; test equations as soon as defined.
 for(I c=0;c<=M;++c)for(I d=0;d<=M;++d)for(I e=0;e<=M;++e)for(I f=0;f<=M;++f){
  if(-c*c+d*d-e*e+f*f-1!=0)continue;
  for(I b=0;b<=M;++b){
   if(b*(c-d)+d*(e-f)!=0)continue;
   for(I a=0;a<=M;++a){
    if(a*c-b*b+2*b*e-c*c-d*d+1!=0||a*d-b*b+b*e+b*f-2*c*d!=0)continue;
    if(final_dimension&&!bounded(tensor_n(a,b,c,d,e,f),D))continue;
    std::cout<<"N "<<a<<' '<<b<<' '<<c<<' '<<d<<' '<<e<<' '<<f<<'\n';
   }
  }
 }
}

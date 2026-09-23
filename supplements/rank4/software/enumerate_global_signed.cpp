// Complete bounded signed self-dual rank-four associative tables, modulo
// sign changes of the three nonunit basis vectors and their permutations.
// Usage: enumerate_global_signed BOUND [THREADS]. Stdout: S + ten integers.
// Output order can vary with thread scheduling; the representative set cannot.
// Compile: g++ -O3 -std=c++17 -fopenmp enumerate_global_signed.cpp -o enum
// All bounds and eliminations are integral, with signed 128-bit modular products.
#include <algorithm>
#include <array>
#include <chrono>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <vector>
#include <omp.h>
using I=long long;using P=std::array<I,10>;
bool valid(const P&p){auto[a,b,c,d,e,f,g,h,i,j]=p;return
 a*d-b*b+b*g+c*h-d*d-e*e+1==0&&a*e-b*c+b*h+c*i-d*e-e*f==0&&
 b*e-c*d+d*h-e*g+e*i-f*h==0&&a*f+b*i-c*c+c*j-e*e-f*f+1==0&&
 b*f-c*e+d*i-e*h+e*j-f*i==0&&d*f-e*e+g*i-h*h+h*j-i*i+1==0;}
I mod(I a,I n){I r=a%n;return r<0?r+n:r;}
I inverse(I a,I n){I r0=n,r1=mod(a,n),x0=0,x1=1;while(r1){I q=r0/r1,r=r0-q*r1,x=x0-q*x1;r0=r1;r1=r;x0=x1;x1=x;}if(r0!=1)throw std::logic_error("noninvertible");return mod(x0,n);}
I floor_div(I a,I b){I q=a/b,r=a%b;return q-(r<0);}
I ceil_div(I a,I b){return -floor_div(-a,b);}
int main(int argc,char**argv){
 if(argc<2||argc>3)throw std::invalid_argument("usage: BOUND [THREADS]");
 I M=std::stoll(argv[1]);int threads=argc>2?std::stoi(argv[2]):1;
 if(threads<1||threads>256)throw std::invalid_argument("thread guard");
 omp_set_num_threads(threads);bool counts=false;I n=0,raw=0;
 I loops=2*(2*M+1)*(M*(M+1)/2)*(M*(M+1)/2);
 if(M<1||M>1000)throw std::invalid_argument("bound");
 auto start=std::chrono::steady_clock::now();
 auto has=[&](I v){return std::abs(v)<=M;};
 const std::array<std::array<int,3>,10> triples{{{0,0,0},{0,0,1},{0,0,2},{0,1,1},{0,1,2},{0,2,2},{1,1,1},{1,1,2},{1,2,2},{2,2,2}}};
 const std::array<int,10> masks{{1,2,4,1,7,1,2,4,2,4}};
 std::vector<std::array<int,10>> maps;std::array<int,3> perm{0,1,2};
 do{std::array<int,10> map{};for(int k=0;k<10;++k){std::array<int,3> tri{perm[triples[k][0]],perm[triples[k][1]],perm[triples[k][2]]};std::sort(tri.begin(),tri.end());map[k]=std::find(triples.begin(),triples.end(),tri)-triples.begin();}maps.push_back(map);}while(std::next_permutation(perm.begin(),perm.end()));
 auto preferred=[&](const P&p){return p[1]>=0&&p[2]>=0&&p[3]>=0&&p[1]<=std::abs(p[2])&&p[1]<=std::abs(p[3])&&p[1]<=std::abs(p[5])&&p[1]<=std::abs(p[7])&&p[1]<=std::abs(p[8])&&(!(p[1]==0&&p[2]==0)||p[4]>=0);};
 auto emit=[&](const P&p){if(!valid(p))return;
  #pragma omp atomic update
  ++raw;if(!preferred(p))throw std::logic_error("not preferred");
  for(const auto&map:maps)for(int mask=0;mask<8;++mask){P q;for(int k=0;k<10;++k)q[k]=p[map[k]]*((__builtin_popcount(mask&masks[k])%2)?-1:1);if(preferred(q)&&q<p)return;}
  #pragma omp atomic update
  ++n;if(!counts){
   #pragma omp critical(output)
   {std::cout<<"S";for(I v:p)std::cout<<' '<<v;std::cout<<'\n';}}
 };
 #pragma omp parallel for schedule(dynamic,1)
 for(I b=1;b<=M;++b)for(I c=b;c<=M;++c)for(I d=b;d<=M;++d)for(I e=-M;e<=M;++e)for(I ff=b;ff<=M;++ff)for(int fs:{-1,1}){I f=fs*ff;
  I H0=e*(d+f)+b*c,G0=b*b+d*d+e*e-1,J0=c*c+e*e+f*f-1;
  // Interval hulls of the signed coordinate domains are necessary bounds.
  if(std::abs(H0)>M*(std::abs(e)+b+c)||G0>M*(d+b+c)||J0>M*(std::abs(f)+b+c))continue;
  I A=e*(b*b-c*c)+b*c*(f-d),C=e*(b*f-c*e);
  I B0=b*b*b*e-b*b*c*d+b*(d-f)*H0-e*b*G0+e*c*H0;
  if(std::abs(B0)>M*(std::abs(C)+std::abs(A)))continue;
  auto finish=[&](I a,I i){
   if(!has(i)||std::abs(i)<b)return;I hh=H0-a*e-c*i;if(hh%b)return;I h=hh/b;if(!has(h)||std::abs(h)<b)return;
   I gg=G0-a*d-c*h;if(gg%b)return;I g=gg/b;if(!has(g))return;I jj=J0-a*f-b*i;if(jj%c)return;I j=jj/c;if(!has(j))return;emit({a,b,c,d,e,f,g,h,i,j});
  };
  if(A){I div=std::gcd(A,C);if(B0%div)continue;I step=std::abs(A/div),a0=0;
   if(step>1)a0=static_cast<I>((static_cast<__int128>(mod(-B0/div,step))*inverse(C/div,step))%step);
   for(I a=-M+mod(a0+M,step);a<=M;a+=step){I rhs=-B0-C*a;if(rhs%A==0)finish(a,rhs/A);}
  }else if(C){if(B0%C==0&&has(-B0/C))for(I i=-M;i<=M;++i)finish(-B0/C,i);}
  else if(B0==0)for(I a=-M;a<=M;++a)for(I i=-M;i<=M;++i)finish(a,i);
 }
 std::cerr<<"dense "<<M<<' '<<loops<<' '<<n<<' '<<raw<<' '<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<'\n';
 // b=0<c,e!=0. Congruence e(d+f-a)=0 (mod c) fixes a progression.
 #pragma omp parallel for schedule(dynamic,1)
 for(I c=1;c<=M;++c)for(I d=0;d<=M;++d)for(I e=-M;e<=M;++e)if(e){I step=c/std::gcd(c,e);
  for(I f=-M;f<=M;++f){I W=c*M/std::abs(e),lo=std::max(-M,d+f-W),hi=std::min(M,d+f+W);
   auto restrict_a=[&](I q,I numerator){if(q<0){q=-q;numerator=-numerator;}if(q){lo=std::max(lo,ceil_div(numerator-c*M,q));hi=std::min(hi,floor_div(numerator+c*M,q));}else if(std::abs(numerator)>c*M){lo=1;hi=0;}};
   restrict_a(d,d*d+e*e-1);restrict_a(f,c*c+e*e+f*f-1);if(lo>hi)continue;
   for(I a=lo+mod(d+f-lo,step);a<=hi;a+=step){I hh=d*d+e*e-a*d-1,ii=e*(d+f-a),jj=c*c+e*e+f*f-a*f-1;if(hh%c||ii%c||jj%c)continue;I h=hh/c,i=ii/c,j=jj/c;if(!has(h)||!has(i)||!has(j))continue;I gg=h*(d-f)+e*i-c*d;if(gg%e==0&&has(gg/e))emit({a,0,c,d,e,f,gg/e,h,i,j});}
  }
 }
 // b=0<c,e=0,d>0. Coprimality and h(d-f)=cd.
 #pragma omp parallel for schedule(dynamic,1)
 for(I c=1;c<=M;++c)for(I d=1;d<=M;++d){if(std::gcd(c,d)!=1)continue;I a0=c==1?0:mod(d-inverse(d,c),c);
  for(I a=-M+mod(a0+M,c);a<=M;a+=c){I hh=d*d-a*d-1;if(!hh||hh%c)continue;I h=hh/c;if(!has(h)||c*d%h)continue;I f=d-c*d/h;if(!has(f))continue;I jj=c*c+f*f-a*f-1;if(jj%c)continue;I j=jj/c;if(!has(j))continue;for(I g=-M;g<=M;++g)emit({a,0,c,d,0,f,g,h,0,j});}}
 // b=0<c,e=d=0 forces c=1,h=-1,f=i=j=0.
 #pragma omp parallel for schedule(dynamic,1)
 for(I a=-M;a<=M;++a)for(I g=-M;g<=M;++g)emit({a,0,1,0,0,0,g,-1,0,0});
 // b=c=0<e: a=d+f and df=e^2-1.
 #pragma omp parallel for schedule(dynamic,1)
 for(I e=1;e<=M;++e)for(I d=0;d<=M;++d){I rhs=e*e-1;auto finish=[&](I f){I a=d+f;if(!has(f)||!has(a))return;
  for(I h=-M;h<=M;++h)for(I i=-M;i<=M;++i){I gg=h*(d-f)+e*i,jj=e*h+i*(f-d);if(gg%e==0&&jj%e==0&&has(gg/e)&&has(jj/e))emit({a,0,0,d,e,f,gg/e,h,i,jj/e});}};
  if(d){if(rhs%d==0)finish(rhs/d);}else if(rhs==0)for(I f=-M;f<=M;++f)finish(f);
 }
 // b=c=e=0,d=1,a=0,f=+/-1.
 #pragma omp parallel for schedule(dynamic,1)
 for(I h=-M;h<=M;++h)for(I i=-M;i<=M;++i){I rhs=h*h+i*i-2;if(h){for(I g=-M;g<=M;++g){I jj=rhs-g*i;if(jj%h==0&&has(jj/h))emit({0,0,0,1,0,1,g,h,i,jj/h});}}else if(i&&rhs%i==0&&has(rhs/i))for(I j=-M;j<=M;++j)emit({0,0,0,1,0,1,rhs/i,0,i,j});}
 #pragma omp parallel for schedule(dynamic,1)
 for(I g=-M;g<=M;++g)for(I j=-M;j<=M;++j)emit({0,0,0,1,0,-1,g,0,0,j});
 std::cerr<<"done "<<M<<' '<<loops<<' '<<n<<' '<<raw<<' '<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<'\n';
}

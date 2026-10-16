// Exact bounded enumeration. See verification_guide.pdf for elimination proof.
#include <array>
#include <iostream>
#include <sstream>
#include <string>
#include <stdexcept>
#include <vector>
using P=std::array<long long,10>;
using Wide=__int128_t;
void put_wide(Wide v){
 if(v<0)throw std::runtime_error("negative count");
 std::string digits;do{digits.push_back(char('0'+v%10));v/=10;}while(v);
 for(auto it=digits.rbegin();it!=digits.rend();++it)std::cout<<*it;
}
// Exact determinant of the Casimir Gram matrix.  The Schur complement
// uses C_00=4.  Every entry of 4*C_ij-C_i0*C_0j is bounded by 73*M^2
// for M>=1, hence the six determinant terms fit in signed 128 bits at
// the enforced bound M<=1000. No modular inverse or floating point is used.
Wide casimir_det(const P&p){
 auto[a,b,c,d,e,f,g,h,i,j]=p;
 Wide x=a+d+f,y=b+g+i,z=c+h+j;
 Wide B11=2+a*a+2*b*b+2*c*c+d*d+2*e*e+f*f;
 Wide B22=2+b*b+2*d*d+2*e*e+g*g+2*h*h+i*i;
 Wide B33=2+c*c+2*e*e+2*f*f+h*h+2*i*i+j*j;
 Wide B12=a*b+2*b*d+2*c*e+d*g+2*e*h+f*i;
 Wide B13=a*c+2*b*e+2*c*f+d*h+2*e*i+f*j;
 Wide B23=b*c+2*d*e+2*e*f+g*h+2*h*i+i*j;
 Wide A=4*B11-x*x,B=4*B22-y*y,C=4*B33-z*z;
 Wide D=4*B12-x*y,E=4*B13-x*z,F=4*B23-y*z;
 Wide det=A*B*C+2*D*E*F-A*F*F-B*E*E-C*D*D;
 if(det%16)throw std::runtime_error("nonintegral determinant");
 return det/16;
}
bool parity_failure(const P&N,const P&p){
 constexpr int slots[3][3]={{0,3,5},{1,6,8},{2,7,9}};
 for(const auto& row:slots){bool plus=true,minus=true;
  for(int k:row){plus=plus&&((N[k]-p[k])%4==0);minus=minus&&((N[k]+p[k])%4==0);}
  if(!plus&&!minus)return true;
 }return false;
}
bool valid(const P&p){auto[a,b,c,d,e,f,g,h,i,j]=p;return
 a*d-b*b+b*g+c*h-d*d-e*e+1==0&&a*e-b*c+b*h+c*i-d*e-e*f==0&&b*e-c*d+d*h-e*g+e*i-f*h==0&&a*f+b*i-c*c+c*j-e*e-f*f+1==0&&b*f-c*e+d*i-e*h+e*j-f*i==0&&d*f-e*e+g*i-h*h+h*j-i*i+1==0;}
int main(){std::string line;while(std::getline(std::cin,line)){
 std::istringstream in(line);int n;if(!(in>>n))continue;
 P N;for(long long &v:N){if(!(in>>v)||v<0||v>1000)throw std::runtime_error("coefficient guard");}std::array<std::vector<long long>,10>D;
 std::array<bool,10>pos={};for(int k=0;k<10;++k){int v;if(!(in>>v)||(v!=0&&v!=1))throw std::runtime_error("gauge input");pos[k]=v;}
 int filtered=0,np=0;std::vector<long long>primes;
 if(in>>filtered){if(!(in>>np)||np<0||(filtered!=0&&filtered!=1))throw std::runtime_error("prime count");for(int k=0;k<np;++k){long long q;if(!(in>>q)||q<2)throw std::runtime_error("prime guard");primes.push_back(q);}}
 for(int k=0;k<10;++k)for(long long v=-N[k];v<=N[k];v+=2)if(!pos[k]||v>0)D[k].push_back(v);
 auto has=[&](int k,long long v){return v>=-N[k]&&v<=N[k]&&(v+N[k])%2==0&&(!pos[k]||v>0);};
 // At most (M+1)^8 terminal candidates, even in the zero-denominator
 // branches. Wide counters therefore also satisfy the M<=1000 guard.
 Wide outer=0,done=0,count=0,det_rejected=0,parity_rejected=0,retained=0;
 std::vector<Wide>prime_counts(primes.size());
 auto emit=[&](P p){++done;if(valid(p)){++count;
  if(filtered){Wide det=casimir_det(p);for(size_t k=0;k<primes.size();++k)if(det%primes[k]){++det_rejected;++prime_counts[k];return;}
   if(parity_failure(N,p)){++parity_rejected;return;}}
  ++retained;std::cout<<"T "<<n;for(long long v:p)std::cout<<' '<<v;std::cout<<'\n';}};
 for(long long a:D[0])for(long long b:D[1])for(long long c:D[2])for(long long d:D[3])for(long long e:D[4])for(long long f:D[5]){
  if(b){
   long long H=e*(d+f-a)+b*c,G=b*b+d*d+e*e-a*d-1,J=c*c+e*e+f*f-a*f-1;
   auto finish=[&](long long i){++outer;long long hh=H-c*i;if(hh%b)return;
    long long h=hh/b;if(!has(7,h))return;long long gg=G-c*h;if(gg%b)return;
    long long g=gg/b;if(!has(6,g))return;long long jj=J-b*i;
    if(c){if(jj%c)return;long long j=jj/c;if(has(9,j))emit({a,b,c,d,e,f,g,h,i,j});}
    else if(jj==0)for(long long j:D[9])emit({a,b,c,d,e,f,g,h,i,j});
   };
   if(c){
    long long A=e*(b*b-c*c)+b*c*(f-d);
    long long B=b*b*b*e-b*b*c*d+b*(d-f)*H-e*b*G+e*c*H;
    if(A){if(B%A==0&&has(8,-B/A))finish(-B/A);}
    else if(B==0)for(long long i:D[8])finish(i);
   }else if(J%b==0&&has(8,J/b))finish(J/b);
  }else if(c){++outer;long long hh=d*d+e*e-a*d-1,ii=e*(d+f-a),jj=c*c+e*e+f*f-a*f-1;if(hh%c||ii%c||jj%c)continue;long long h=hh/c,i=ii/c,j=jj/c;if(!has(7,h)||!has(8,i)||!has(9,j))continue;long long gg=h*(d-f)+e*i-c*d;
   if(e){if(gg%e)continue;long long g=gg/e;if(!has(6,g))continue;emit({a,b,c,d,e,f,g,h,i,j});}else if(gg==0){for(long long g:D[6])emit({a,b,c,d,e,f,g,h,i,j});}
  }else{++outer;
   if(a*d-d*d-e*e+1 || e*(a-d-f) || a*f-e*e-f*f+1)continue;
   for(long long h:D[7])for(long long i:D[8]){
    long long gg=h*(d-f)+e*i,jj=e*h+i*(f-d);
    if(e){if(gg%e||jj%e)continue;long long g=gg/e,j=jj/e;if(has(6,g)&&has(9,j))emit({a,b,c,d,e,f,g,h,i,j});}
    else if(gg==0&&jj==0){for(long long g:D[6])for(long long j:D[9])emit({a,b,c,d,e,f,g,h,i,j});}
   }
  }
 }
 std::cout<<"C "<<n<<' ';put_wide(outer);std::cout<<' ';put_wide(done);std::cout<<' ';put_wide(count);
 if(filtered){std::cout<<' ';put_wide(det_rejected);std::cout<<' ';put_wide(parity_rejected);std::cout<<' ';put_wide(retained);for(Wide v:prime_counts){std::cout<<' ';put_wide(v);}}
 std::cout<<'\n';
}return 0;}

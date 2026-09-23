// Exact bounded enumeration. See verification_guide.pdf for elimination proof.
#include <algorithm>
#include <numeric>
#include <array>
#include <cstdint>
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

long long residue(long long a,long long m){long long r=a%m;return r<0?r+m:r;}
long long inverse_mod(long long a,long long m){
 long long r0=m,r1=residue(a,m),x0=0,x1=1;
 while(r1){long long q=r0/r1,r=r0-q*r1,x=x0-q*x1;r0=r1;r1=r;x0=x1;x1=x;}
 if(r0!=1)throw std::logic_error("noninvertible residue");return residue(x0,m);
}
int main(){std::string line;while(std::getline(std::cin,line)){
 std::istringstream in(line);int n;if(!(in>>n))continue;
 P N;for(long long &v:N){if(!(in>>v)||v<0||v>1000)throw std::runtime_error("coefficient guard");}
 std::array<bool,10>pos={};for(int k=0;k<10;++k){int v;if(!(in>>v)||(v!=0&&v!=1))throw std::runtime_error("gauge input");pos[k]=v;}
 int filtered=0,np=0;std::vector<long long>primes;
 if(in>>filtered){if(!(in>>np)||np<0||filtered<0||filtered>2)throw std::runtime_error("prime count");for(int k=0;k<np;++k){long long q;if(!(in>>q)||q<2)throw std::runtime_error("prime guard");primes.push_back(q);}}
 // Mode 2 applies the necessary adjoint-parity criterion before enumeration.
 // Each row sign gives one residue class modulo 4. Distinct residue boxes
 // are disjoint, and their union is exactly the parity-admissible domain.
 std::vector<std::array<int,10>>boxes;
 if(filtered==2){
  constexpr int slots[3][3]={{0,3,5},{1,6,8},{2,7,9}};
  for(int mask=0;mask<8;++mask){std::array<int,10>r;r.fill(-1);
   for(int row=0;row<3;++row){long long sign=(mask&(1<<row))?1:-1;
    for(int k:slots[row])r[k]=residue(sign*N[k],4);}
   if(std::find(boxes.begin(),boxes.end(),r)==boxes.end())boxes.push_back(r);
  }
 }else{std::array<int,10>r;r.fill(-1);boxes.push_back(r);}
 Wide outer=0,done=0,count=0,det_rejected=0,parity_rejected=0,retained=0;
 std::vector<Wide>prime_counts(primes.size());long long nonempty_boxes=0;
 auto emit=[&](P p){++done;if(valid(p)){++count;
  if(filtered){Wide det=casimir_det(p);for(size_t k=0;k<primes.size();++k)if(det%primes[k]){++det_rejected;++prime_counts[k];return;}
   if(parity_failure(N,p)){if(filtered==2)throw std::logic_error("parity box failed");++parity_rejected;return;}}
  ++retained;std::cout<<"T "<<n;for(long long v:p)std::cout<<' '<<v;std::cout<<'\n';}};
 for(const auto&r:boxes){
  std::array<std::vector<long long>,10>D;std::array<long long,10>steps;
  bool empty=false;
  for(int k=0;k<10;++k){steps[k]=r[k]<0?2:4;
   for(long long v=-N[k];v<=N[k];v+=2)
    if((!pos[k]||v>0)&&(r[k]<0||residue(v,4)==r[k]))D[k].push_back(v);
   if(D[k].empty())empty=true;
  }
  if(empty)continue;++nonempty_boxes;
  auto has=[&](int k,long long v){return v>=D[k].front()&&v<=D[k].back()&&(v-D[k].front())%steps[k]==0;};
  // Exact modular projection: a genuine solution reduces to a solution
  // of all six associativity equations modulo 16.  For each parity box,
  // enumerate its (at most four/eight) residues in each variable and
  // project the modular solution set onto (b,c,d,e,f,a,i).  The first
  // five coordinates index the table; the final two are a 16-bit mask.
  // This is a necessary congruence test, never a replacement for valid().
  std::vector<std::array<long long,6>>feasible;
  std::array<std::array<std::vector<long long>,16>,10>groups;
  std::array<int,16>ar{},ir{};int ni=0;
  if(filtered==2){
   std::array<std::vector<long long>,10>V;
   for(int k=0;k<10;++k){for(long long v:D[k]){long long q=residue(v,16);groups[k][q].push_back(v);
     if(std::find(V[k].begin(),V[k].end(),q)==V[k].end())V[k].push_back(q);}
    std::sort(V[k].begin(),V[k].end());}
   ni=V[8].size();for(int k=0;k<int(V[0].size());++k)ar[V[0][k]]=k;
   for(int k=0;k<ni;++k)ir[V[8][k]]=k;
   for(long long b:V[1])for(long long c:V[2])for(long long d:V[3])for(long long e:V[4])for(long long f:V[5]){
    std::uint16_t mask=0;
    for(long long a:V[0])for(long long h:V[7])for(long long g:V[6]){
     if((a*d-b*b+b*g+c*h-d*d-e*e+1)%16)continue;
     for(long long i:V[8]){
      if((a*e-b*c+b*h+c*i-d*e-e*f)%16||(b*e-c*d+d*h-e*g+e*i-f*h)%16)continue;
      for(long long j:V[9]){
       if((a*f+b*i-c*c+c*j-e*e-f*f+1)%16||(b*f-c*e+d*i-e*h+e*j-f*i)%16||
          (d*f-e*e+g*i-h*h+h*j-i*i+1)%16)continue;
       mask|=std::uint16_t(1)<<(ar[a]*ni+ir[i]);break;
      }
     }
    }
    if(mask)feasible.push_back({b,c,d,e,f,mask});
   }
  }
  // Solve C*a+A*i=rhs on the exact arithmetic-progression domains.
  // Substitute a=a0+sa*u, i=i0+si*v, then use a complete gcd progression.
  // Every singular coefficient case is retained. The modular product uses
  // 128 bits; all other elimination expressions fit int64 for M<=1000.
  auto solve=[&](long long C,long long A,long long rhs,auto&& finish){
   long long amin=D[0].front(),amax=D[0].back(),imin=D[8].front(),imax=D[8].back();
   long long lo=std::min(C*amin,C*amax)+std::min(A*imin,A*imax);
   long long hi=std::max(C*amin,C*amax)+std::max(A*imin,A*imax);
   if(rhs<lo||rhs>hi)return;
   long long U=C*steps[0],V=A*steps[8],T=rhs-C*amin-A*imin;
   long long nu=D[0].size()-1,nv=D[8].size()-1;
   if(V){
    long long g=std::gcd(U,V);if(T%g)return;
    long long step=std::abs(V/g),u0=0;
    if(step>1)u0=(static_cast<Wide>(residue(T/g,step))*inverse_mod(U/g,step))%step;
    for(long long u=u0;u<=nu;u+=step){long long vv=T-U*u;
     if(vv%V)throw std::logic_error("invalid gcd progression");long long v=vv/V;
     if(0<=v&&v<=nv)finish(amin+steps[0]*u,imin+steps[8]*v);
    }
   }else if(U){if(T%U==0){long long u=T/U;if(0<=u&&u<=nu)for(long long i:D[8])finish(amin+steps[0]*u,i);}}
   else if(T==0)for(long long a:D[0])for(long long i:D[8])finish(a,i);
  };
  auto enumerate_free=[&](long long b,long long c,long long d,long long e,long long f,std::uint16_t mask){
   if(b){
    long long H0=e*(d+f)+b*c,G0=b*b+d*d+e*e-1,J0=c*c+e*e+f*f-1;
    auto finish=[&](long long a,long long i){++outer;
     if(filtered==2&&!(mask&(std::uint16_t(1)<<(ar[residue(a,16)]*ni+ir[residue(i,16)]))))return;
     long long hh=H0-a*e-c*i;if(hh%b)return;long long h=hh/b;if(!has(7,h))return;
     long long gg=G0-a*d-c*h;if(gg%b)return;long long g=gg/b;if(!has(6,g))return;
     long long jj=J0-a*f-b*i;
     if(c){if(jj%c)return;long long j=jj/c;if(has(9,j))emit({a,b,c,d,e,f,g,h,i,j});}
     else if(jj==0)for(long long j:D[9])emit({a,b,c,d,e,f,g,h,i,j});
    };
    if(c){
     long long A=e*(b*b-c*c)+b*c*(f-d),C=e*(b*f-c*e);
     long long B0=b*b*b*e-b*b*c*d+b*(d-f)*H0-e*b*G0+e*c*H0;
     solve(C,A,-B0,finish);
    }else solve(f,b,J0,finish);
   }else if(c){
    for(long long a:D[0]){++outer;
     long long hh=d*d+e*e-a*d-1,ii=e*(d+f-a),jj=c*c+e*e+f*f-a*f-1;
     if(hh%c||ii%c||jj%c)continue;long long h=hh/c,i=ii/c,j=jj/c;
     if(!has(7,h)||!has(8,i)||!has(9,j))continue;long long gg=h*(d-f)+e*i-c*d;
     if(e){if(gg%e)continue;long long g=gg/e;if(has(6,g))emit({a,b,c,d,e,f,g,h,i,j});}
     else if(gg==0)for(long long g:D[6])emit({a,b,c,d,e,f,g,h,i,j});
    }
   }else{
    // If e!=0, e(a-d-f)=0 fixes a. If e=0, the first
    // equation fixes a=(d^2-1)/d and d=0 is impossible.
    long long a;
    if(e)a=d+f;else{if(!d||(d*d-1)%d)return;a=(d*d-1)/d;}
    if(!has(0,a))return;++outer;
    if(a*d-d*d-e*e+1||e*(a-d-f)||a*f-e*e-f*f+1)return;
    for(long long h:D[7])for(long long i:D[8]){
     long long gg=h*(d-f)+e*i,jj=e*h+i*(f-d);
     if(e){if(gg%e||jj%e)continue;long long g=gg/e,j=jj/e;if(has(6,g)&&has(9,j))emit({a,b,c,d,e,f,g,h,i,j});}
     else if(gg==0&&jj==0)for(long long g:D[6])for(long long j:D[9])emit({a,b,c,d,e,f,g,h,i,j});
    }
   }
  };
  if(filtered==2){
   // Enumerate only feasible residue classes, so the modular sieve also
   // removes outer iterations rather than merely avoiding gcd calls.
   for(const auto&q:feasible)
    for(long long b:groups[1][q[0]])for(long long c:groups[2][q[1]])
    for(long long d:groups[3][q[2]])for(long long e:groups[4][q[3]])
    for(long long f:groups[5][q[4]])enumerate_free(b,c,d,e,f,q[5]);
  }else for(long long b:D[1])for(long long c:D[2])for(long long d:D[3])
    for(long long e:D[4])for(long long f:D[5])enumerate_free(b,c,d,e,f,0);
 }
 if(filtered==2)std::cout<<"B "<<n<<' '<<nonempty_boxes<<'\n';
 std::cout<<"C "<<n<<' ';put_wide(outer);std::cout<<' ';put_wide(done);std::cout<<' ';put_wide(count);
 if(filtered){std::cout<<' ';put_wide(det_rejected);std::cout<<' ';put_wide(parity_rejected);std::cout<<' ';put_wide(retained);for(Wide v:prime_counts){std::cout<<' ';put_wide(v);}}
 std::cout<<'\n';
}return 0;}

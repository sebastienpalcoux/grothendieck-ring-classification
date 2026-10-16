// Exact non-self-dual signed enumeration. Equation four determines f^2;
// equation three determines b unless c=d, and equations one or two then
// determine a. Every zero denominator is treated separately.
#include <array>
#include <iostream>
#include <set>
#include <stdexcept>
#include <vector>
using P=std::array<long long,6>;
bool valid(const P&p){auto[a,b,c,d,e,f]=p;return
 a*c-b*b+2*b*e-c*c-d*d+1==0&&a*d-b*b+b*e+b*f-2*c*d==0&&
 b*(c-d)+d*(e-f)==0&&-c*c+d*d-e*e+f*f-1==0;}
P gauge(const P&p){auto[a,b,c,d,e,f]=p;P ans=p;
 for(int u:{-1,1})for(int v:{-1,1})ans=std::min(ans,P{u*a,v*b,u*c,u*d,v*e,v*f});
 return ans;}
int main(){P N;while(std::cin>>N[0]){
 for(int k=1;k<6;++k)if(!(std::cin>>N[k]))throw std::runtime_error("incomplete coefficients");
 for(long long n:N)if(n<0||n>1000)throw std::runtime_error("coefficient guard");
 std::array<std::vector<long long>,6>D;
 for(int k=0;k<6;++k)for(long long v=-N[k];v<=N[k];v+=2)D[k].push_back(v);
 auto has=[&](int k,long long v){return v>=-N[k]&&v<=N[k]&&(v+N[k])%2==0;};
 std::vector<int>roots(N[5]*N[5]+1,-1);
 for(long long f:D[5])roots[f*f]=f<0?-f:f;
 std::set<P>out;
 auto emit=[&](const P&p){if(valid(p))out.insert(gauge(p));};
 for(long long c:D[2])for(long long d:D[3])for(long long e:D[4]){
  long long square=e*e+c*c-d*d+1;
  if(square<0||square>=(long long)roots.size()||roots[square]<0)continue;
  long long r=roots[square];
  for(long long f:std::vector<long long>(r?std::initializer_list<long long>{-r,r}:std::initializer_list<long long>{0})){
   auto finish=[&](long long b){
    if(!has(1,b))return;
    if(c){long long rhs=b*b-2*b*e+c*c+d*d-1;if(rhs%c==0&&has(0,rhs/c))emit({rhs/c,b,c,d,e,f});}
    else if(d){long long rhs=b*b-b*e-b*f+2*c*d;if(rhs%d==0&&has(0,rhs/d))emit({rhs/d,b,c,d,e,f});}
    else for(long long a:D[0])emit({a,b,c,d,e,f});
   };
   if(c!=d){long long rhs=d*(f-e);if(rhs%(c-d)==0)finish(rhs/(c-d));}
   else if(d*(e-f)==0)for(long long b:D[1])finish(b);
  }
 }
 for(const P&p:out){std::cout<<"T";for(long long v:p)std::cout<<' '<<v;std::cout<<'\n';}
 std::cout<<"C "<<out.size()<<'\n';
}return 0;}

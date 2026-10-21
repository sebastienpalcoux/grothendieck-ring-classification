#include <algorithm>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <vector>
using I=long long;
struct Row { I constant,low,high,mod;std::vector<I>a; };
int n;std::vector<Row>rows;std::uint64_t nodes=0;std::vector<std::vector<I>>solutions;
I floor_div(I a,I b){if(b<=0)throw std::runtime_error("denominator");I q=a/b,r=a%b;return q-(r<0);}
I ceil_div(I a,I b){return -floor_div(-a,b);}
bool propagate(std::vector<I>&lo,std::vector<I>&hi){
 bool changed=true;
 while(changed){changed=false;
  for(const auto&r:rows){
   I mn=r.constant,mx=r.constant;
   for(int j=0;j<n;j++){mn+=r.a[j]*(r.a[j]>=0?lo[j]:hi[j]);mx+=r.a[j]*(r.a[j]>=0?hi[j]:lo[j]);}
   if(mx<r.low||mn>r.high)return false;
   I fixed=r.constant,g=r.mod;
   for(int j=0;j<n;j++)if(lo[j]==hi[j])fixed+=r.a[j]*lo[j];else g=std::gcd(g,std::abs(r.a[j]));
   if(g&&fixed%g)return false;
   for(int j=0;j<n;j++)if(r.a[j]&&lo[j]!=hi[j]){
    I c=r.a[j],omin=mn-c*(c>0?lo[j]:hi[j]),omax=mx-c*(c>0?hi[j]:lo[j]);
    I a,b;if(c>0){a=ceil_div(r.low-omax,c);b=floor_div(r.high-omin,c);}
    else{a=ceil_div(omin-r.high,-c);b=floor_div(omax-r.low,-c);}
    a=std::max(a,lo[j]);b=std::min(b,hi[j]);if(a>b)return false;
    if(a!=lo[j]||b!=hi[j]){lo[j]=a;hi[j]=b;changed=true;break;}
   }
   if(changed)break;
  }
 }
 return true;
}
void visit(std::vector<I>lo,std::vector<I>hi){
 if(++nodes==0)throw std::runtime_error("node counter overflow");
 if(!propagate(lo,hi))return;
 int at=-1;
 for(int j=0;j<n;j++)if(lo[j]<hi[j]&&(at<0||hi[j]-lo[j]<hi[at]-lo[at]))at=j;
 if(at<0){solutions.push_back(lo);return;}
 I top=hi[at];for(I x=lo[at];x<=top;x++){auto ll=lo,hh=hi;ll[at]=hh[at]=x;visit(ll,hh);}
}
int main(){
 int nr;std::cin>>n>>nr;if(n<0||n>100||nr<0||nr>500)throw std::runtime_error("input size");
 std::vector<I>lo(n),hi(n);for(auto&x:hi)std::cin>>x;
 for(int i=0;i<nr;i++){Row r;std::cin>>r.constant>>r.low>>r.high>>r.mod;r.a.resize(n);for(auto&x:r.a)std::cin>>x;rows.push_back(r);}
 visit(lo,hi);std::sort(solutions.begin(),solutions.end());
 if(std::adjacent_find(solutions.begin(),solutions.end())!=solutions.end())throw std::runtime_error("duplicate solution");
 std::cout<<"{\"nodes\":"<<nodes<<",\"solutions\":[";
 for(size_t i=0;i<solutions.size();i++){if(i)std::cout<<",";std::cout<<"[";for(int j=0;j<n;j++){if(j)std::cout<<",";std::cout<<solutions[i][j];}std::cout<<"]";}
 std::cout<<"]}\n";
}

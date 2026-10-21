// Exact row-sum meet-in-the-middle, with optional exact Gram pruning.
// Repeated identical column sets are unordered, as in induction.low_matrices.
// PSD uses fraction-free elimination with Python-checked 128-bit bounds.
#include <algorithm>
#include <array>
#include <functional>
#include <iostream>
#include <map>
#include <vector>
using Z=__int128_t;
using V=std::vector<int>;
using Choice=std::array<int,8>;
int d,k,prune; V target;std::vector<std::vector<V>> cols;
std::vector<std::vector<long long>> B;std::vector<std::vector<bool>> same;
bool psd(const Choice& c){
 std::vector<std::vector<Z>> A(d,std::vector<Z>(d));
 for(int i=0;i<d;++i)for(int j=0;j<d;++j){
  long long q=B[i][j];for(int a=0;a<k;++a)if(c[a]>=0)q-=1LL*cols[a][c[a]][i]*cols[a][c[a]][j];
  if(q<0)return false;A[i][j]=q;
 }
 Z prev=1;
 for(int p=0;p<d;++p){
  if(A[p][p]<0)return false;
  if(A[p][p]==0){for(int j=p+1;j<d;++j)if(A[p][j]!=0)return false;continue;}
  Z pivot=A[p][p];
  for(int i=p+1;i<d;++i)for(int j=i;j<d;++j){
   Z z=(pivot*A[i][j]-A[i][p]*A[p][j]);
   if(z%prev!=0){std::cerr<<"nonexact Bareiss division\n";std::exit(3);}
   A[i][j]=z/prev;A[j][i]=A[i][j];
  }
  prev=pivot;
 }
 return true;
}
long double cost(const V& side){
 long double out=1;V done(k);
 for(int a:side)if(!done[a]){int m=0;for(int b:side)if(same[a][b]){done[b]=1;++m;}
  long double c=1;for(int j=1;j<=m;++j)c*=((long double)cols[a].size()+j-1)/j;out*=c;
 }return out;
}
using Emit=std::function<void(const V&,const Choice&)>;
void enumerate(const V& side,const Emit& emit){
 Choice choice;choice.fill(-1);V sum(d);
 auto Q=B;
 std::function<void(int)> dfs=[&](int level){
  if(level==(int)side.size()){if(!prune||psd(choice))emit(sum,choice);return;}
  int a=side[level],lo=0;for(int j=0;j<level;++j)if(same[a][side[j]])lo=choice[side[j]];
  for(int v=lo;v<(int)cols[a].size();++v){bool ok=true;
   for(int i=0;i<d;++i)if(sum[i]+cols[a][v][i]>target[i]){ok=false;break;}
   if(!ok)continue;
   choice[a]=v;for(int i=0;i<d;++i)sum[i]+=cols[a][v][i];
   if(prune){
    for(int i=0;i<d;++i)for(int j=0;j<d;++j)Q[i][j]-=1LL*cols[a][v][i]*cols[a][v][j];
    int remaining=k-level-1;
    for(int i=0;i<d&&ok;++i)for(int j=i;j<d;++j){
     if(Q[i][j]<0){ok=false;break;}
     Z x=Z(remaining)*Q[i][i]-Z(target[i]-sum[i])*(target[i]-sum[i]);
     Z y=Z(remaining)*Q[j][j]-Z(target[j]-sum[j])*(target[j]-sum[j]);
     Z z=Z(remaining)*Q[i][j]-Z(target[i]-sum[i])*(target[j]-sum[j]);
     if(x<0||y<0||x*y<z*z){ok=false;break;}
    }
   }
   if(ok)dfs(level+1);
   if(prune)for(int i=0;i<d;++i)for(int j=0;j<d;++j)Q[i][j]+=1LL*cols[a][v][i]*cols[a][v][j];
   for(int i=0;i<d;++i)sum[i]-=cols[a][v][i];
   choice[a]=-1;
  }
 };dfs(0);
}
int main(){
 if(!(std::cin>>d>>k>>prune)||d<1||d>7||k<1||k>7||(prune!=0&&prune!=1))return 2;
 target.resize(d);for(int& x:target)if(!(std::cin>>x)||x<0||x>1000000)return 2;
 B.assign(d,std::vector<long long>(d));for(auto& row:B)for(auto& x:row)if(!(std::cin>>x)||x<0||x>1000000)return 2;
 cols.resize(k);for(auto& set:cols){int n;if(!(std::cin>>n)||n<0)return 2;set.assign(n,V(d));
  for(auto& v:set)for(int& x:v)if(!(std::cin>>x)||x<0||x>1000000)return 2;
  if(set.empty())return 0;if(!std::is_sorted(set.begin(),set.end()))return 2;
 }
 same.assign(k,std::vector<bool>(k));for(int i=0;i<k;++i)for(int j=0;j<k;++j)same[i][j]=cols[i]==cols[j];
 V left,right;long double best=-1;
 for(int mask=1;mask<(1<<k);++mask)if(mask&1){V a,b;for(int i=0;i<k;++i)(mask>>i&1?a:b).push_back(i);
  long double c=cost(a)+cost(b);if(best<0||c<best){best=c;left=a;right=b;}}
 if(cost(left)>cost(right))std::swap(left,right);
 std::map<V,std::vector<Choice>> buckets;
 enumerate(left,[&](const V& sum,const Choice& c){buckets[sum].push_back(c);});
 enumerate(right,[&](const V& sum,const Choice& c){V need(d);for(int i=0;i<d;++i)need[i]=target[i]-sum[i];
  auto it=buckets.find(need);if(it==buckets.end())return;
  for(const Choice& l:it->second){Choice all=c;for(int i:left)all[i]=l[i];bool ok=true;
   for(int i=0;i<k&&ok;++i)for(int j=i+1;j<k;++j)if(same[i][j]&&all[i]>all[j]){ok=false;break;}
   if(!ok||(prune&&!psd(all)))continue;for(int i=0;i<k;++i)std::cout<<all[i]<<' ';std::cout<<'\n';
  }
 });return 0;
}

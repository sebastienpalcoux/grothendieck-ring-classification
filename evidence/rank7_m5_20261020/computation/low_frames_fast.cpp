// Exact bounded low-induction frames in ranks at most seven.
// Partial entrywise/2x2 PSD tests prune only necessary conditions.
#include <iostream>
#include <vector>
#include <array>
#include <algorithm>
#include <functional>
#include <map>
using W=__int128_t;
int d,k; using V=std::vector<int>; std::vector<std::vector<V>> cols;
std::vector<int> target,order,z;std::vector<V> suffix_min,suffix_max;std::vector<std::map<V,int>> lookup;std::vector<std::vector<int>> B,same;
W det(const std::vector<std::vector<long long>>&Q,const V&idx){
 int n=idx.size();V p(n);for(int i=0;i<n;++i)p[i]=i;W sum=0;
 do{W term=1;int sign=0;for(int i=0;i<n;++i){term*=Q[idx[i]][idx[p[i]]];for(int j=i+1;j<n;++j)sign^=p[i]>p[j];}sum+=sign?-term:term;}while(std::next_permutation(p.begin(),p.end()));return sum;
}
bool psd(const std::vector<std::vector<long long>>&Q,bool full){
 for(int i=0;i<d;++i)for(int j=i;j<d;++j){if(Q[i][j]<0)return false;if(i!=j&&(W)Q[i][i]*Q[j][j]<(W)Q[i][j]*Q[i][j])return false;}
 if(full)for(int mask=1;mask<(1<<d);++mask)if(__builtin_popcount((unsigned)mask)>=3){V ii;for(int i=0;i<d;++i)if(mask>>i&1)ii.push_back(i);if(det(Q,ii)<0)return false;}return true;
}
void dfs(int level,const V&rem,const std::vector<std::vector<long long>>&Q){
 if(level==k){for(int v:rem)if(v)return;if(!psd(Q,true))return;for(int a:z)std::cout<<a<<' ';std::cout<<'\n';return;}
 int c=order[level];
 int begin=0,end=cols[c].size();
 if(level==k-1){auto it=lookup[c].find(rem);if(it==lookup[c].end())return;begin=it->second;end=begin+1;}
 for(int a=begin;a<end;++a){const V&v=cols[c][a];bool ok=true;
  for(int l=0;l<level;++l){int p=order[l];if(same[c][p]&&((p<c&&cols[p][z[p]]>v)||(p>c&&cols[p][z[p]]<v))){ok=false;break;}}
  if(!ok)continue;V r(d);for(int i=0;i<d;++i){r[i]=rem[i]-v[i];if(r[i]<0){ok=false;break;}}if(!ok)continue;
  if(level==k-1){for(int x:r)if(x){ok=false;break;}if(!ok)continue;}
  for(int i=0;i<d&&ok;++i)if(r[i]<suffix_min[level+1][i]||r[i]>suffix_max[level+1][i])ok=false;if(!ok)continue;
  auto qq=Q;for(int i=0;i<d;++i)for(int j=0;j<d;++j)qq[i][j]-=(long long)v[i]*v[j];if(!psd(qq,false))continue;z[c]=a;dfs(level+1,r,qq);
 }
}
int main(){if(!(std::cin>>d>>k)||d<1||d>6||k<1||k>6)return 2;
 target.resize(d);for(int&x:target)std::cin>>x;
 std::vector<std::vector<long long>>Q(d,std::vector<long long>(d));for(auto&row:Q)for(auto&x:row){std::cin>>x;if(x<0||x>1000000)return 2;}
 cols.resize(k);for(auto&c:cols){int n;std::cin>>n;if(n<0)return 2;c.resize(n,V(d));for(auto&v:c)for(int&x:v)std::cin>>x;if(!n)return 0;}
 same.assign(k,V(k));for(int i=0;i<k;++i)for(int j=0;j<k;++j)same[i][j]=cols[i]==cols[j];order.resize(k);z.resize(k);for(int i=0;i<k;++i)order[i]=i;
 std::stable_sort(order.begin(),order.end(),[](int a,int b){return cols[a].size()<cols[b].size();});
 lookup.resize(k);for(int c=0;c<k;++c)for(int a=0;a<(int)cols[c].size();++a)if(!lookup[c].emplace(cols[c][a],a).second)return 4;
 suffix_min.assign(k+1,V(d));suffix_max.assign(k+1,V(d));
 for(int l=k-1;l>=0;--l)for(int i=0;i<d;++i){int mn=1000001,mx=-1;for(const V&w:cols[order[l]]){mn=std::min(mn,w[i]);mx=std::max(mx,w[i]);}suffix_min[l][i]=suffix_min[l+1][i]+mn;suffix_max[l][i]=suffix_max[l+1][i]+mx;}
 dfs(0,target,Q);
}

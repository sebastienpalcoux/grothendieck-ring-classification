// Exact nonnegative integral Gram decompositions into a prescribed finite set.
// Output counts are in input column order. Incomplete runs return nonzero.
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
using V=std::vector<int>;
int n,k;std::vector<V>A;std::vector<std::vector<int>> order_rem;
V order,x;long long nodes=0,solutions=0;bool stopped=false;double limit;
auto start=std::chrono::steady_clock::now();
void dfs(int level,const V&r){
 if(stopped)return;
 if((++nodes&4095)==0 && std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()>limit){stopped=true;return;}
 if(level==k){for(int y:r)if(y)return;for(int y:x)std::cout<<y<<' ';std::cout<<'\n';++solutions;return;}
 int j=order[level],bound=1000000;
 for(int i=0;i<n;++i){if(r[i]<0)return;if(A[j][i])bound=std::min(bound,r[i]/A[j][i]);if(r[i]&&!order_rem[level][i])return;}
 if(bound==1000000)return;
 // A row supported by this variable alone forces its multiplicity.
 int force=-1;
 for(int i=0;i<n;++i)if(A[j][i]&&!order_rem[level+1][i]){if(r[i]%A[j][i])return;int a=r[i]/A[j][i];if(force!=-1&&force!=a)return;force=a;}
 for(int m=(force<0?0:force);m<=(force<0?bound:force);++m){if(m>bound)break;V q=r;for(int i=0;i<n;++i)q[i]-=m*A[j][i];x[j]=m;dfs(level+1,q);}
 x[j]=0;
}
int main(){if(!(std::cin>>n>>k>>limit)||n<1||n>21||k<0||k>20000)return 2;V b(n);for(int&i:b)std::cin>>i;A.resize(k,V(n));for(auto&a:A)for(int&i:a){std::cin>>i;if(i<0||i>1000000)return 2;}
 order.resize(k);x.resize(k);for(int j=0;j<k;++j)order[j]=j;
 // Dense vectors first; sparse columns are solved by forced residual rows.
 std::stable_sort(order.begin(),order.end(),[](int i,int j){int a=0,b=0;for(int v:A[i])a+=v>0;for(int v:A[j])b+=v>0;return a>b;});
 order_rem.assign(k+1,V(n));for(int l=k-1;l>=0;--l)for(int i=0;i<n;++i)order_rem[l][i]=order_rem[l+1][i]+(A[order[l]][i]>0);
 dfs(0,b);std::cerr<<"complete "<<!stopped<<" nodes "<<nodes<<" frames "<<solutions<<'\n';return stopped?3:0;}

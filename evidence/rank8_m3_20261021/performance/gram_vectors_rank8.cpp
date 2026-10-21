// Complete nonnegative integer vectors v with Q-vv^T PSD and entrywise >=0.
// Principal-coordinate prefix ellipsoids prune only necessary conditions.
// Python checks every bound needed for exact signed __int128 arithmetic.
#include <algorithm>
#include <functional>
#include <iostream>
#include <vector>
using I=long long;using W=__int128_t;
int main(){
 int n,r;if(!(std::cin>>n>>r)||n<1||n>8||r<1||r>n)return 2;
 std::vector<std::vector<I>> Q(n,std::vector<I>(n)),M(n,std::vector<I>(r));
 std::vector<int> ix(r);std::vector<I> bound(n),den(r);
 for(auto& row:Q)for(I& x:row)std::cin>>x;
 for(int& x:ix)std::cin>>x;for(I& x:bound)std::cin>>x;
 std::vector<std::vector<std::vector<I>>> adj;
 for(int m=1;m<=r;++m){std::cin>>den[m-1];if(den[m-1]<=0)return 2;
  adj.emplace_back(m,std::vector<I>(m));for(auto& row:adj.back())for(I& x:row)std::cin>>x;}
 for(auto& row:M)for(I& x:row)std::cin>>x;
 std::vector<I>w(r),v(n);
 std::function<void(int)> dfs=[&](int l){
  if(l<r){for(w[l]=0;w[l]<=bound[ix[l]];++w[l]){
   bool ok=true;for(int j=0;j<l;++j)if(W(w[l])*w[j]>Q[ix[l]][ix[j]]){ok=false;break;}if(!ok)continue;
   W z=0;for(int i=0;i<=l;++i)for(int j=0;j<=l;++j)z+=W(w[i])*adj[l][i][j]*w[j];
   if(z<=den[l])dfs(l+1);
  }return;}
  bool nz=false;I det=den.back();
  for(int i=0;i<n;++i){W z=0;for(int j=0;j<r;++j)z+=W(M[i][j])*w[j];
   if(z<0||z%det)return;z/=det;if(z>bound[i])return;v[i]=I(z);nz|=v[i]!=0;}
  if(!nz)return;
  for(int i=0;i<n;++i)for(int j=i;j<n;++j)if(W(v[i])*v[j]>Q[i][j])return;
  for(I x:v)std::cout<<x<<' ';std::cout<<'\n';
 };dfs(0);return 0;
}

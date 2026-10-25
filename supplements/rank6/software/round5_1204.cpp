#include <iostream>
#include <vector>
#include <functional>
using I=long long; using W=__int128_t;
// Exact floor(sqrt(a)) for every nonnegative signed-64-bit input.
// The midpoint avoids signed overflow; its square fits in signed __int128.
I root(I a){I l=0,h=a;while(l<h){I gap=h-l;I m=l+gap/2+gap%2;if(W(m)*m<=a)l=m;else h=m-1;}return l;}
int main(){int n,r;if(!(std::cin>>n>>r)||n<1||n>30||r<1||r>n)return 2;
 std::vector<std::vector<I>>Q(n,std::vector<I>(n)),M(n,std::vector<I>(r));std::vector<int>ix(r);std::vector<I>det(r);std::vector<std::vector<std::vector<I>>>A;
 for(auto&v:Q)for(I&x:v)std::cin>>x;for(int&i:ix)std::cin>>i;for(int k=1;k<=r;++k){std::cin>>det[k-1];if(det[k-1]<=0)return 2;A.push_back(std::vector<std::vector<I>>(k,std::vector<I>(k)));for(auto&v:A.back())for(I&x:v)std::cin>>x;}for(auto&v:M)for(I&x:v)std::cin>>x;
 std::vector<I>fixed(r);for(I&x:fixed)std::cin>>x; std::vector<I>w(r),v(n),bound(r);for(int j=0;j<r;++j)bound[j]=root(Q[ix[j]][ix[j]]);
 std::function<void(int)>dfs=[&](int l){if(l<r){for(w[l]=(fixed[l]>=0?fixed[l]:0);w[l]<=(fixed[l]>=0?fixed[l]:bound[l]);++w[l]){W z=0;for(int i=0;i<=l;++i)for(int j=0;j<=l;++j)z+=W(w[i])*A[l][i][j]*w[j];if(z>det[l])continue;bool good=true;for(int i=0;i<l;++i)if(W(w[i])*w[l]>Q[ix[i]][ix[l]]){good=false;break;}if(good)dfs(l+1);}return;}
 for(int i=0;i<n;++i){W z=0;for(int j=0;j<r;++j)z+=W(M[i][j])*w[j];if(z<0||z%det.back())return;z/=det.back();if(z>root(Q[i][i]))return;v[i]=(I)z;}
 for(int i=0;i<n;++i)for(int j=i;j<n;++j)if(W(v[i])*v[j]>Q[i][j])return;for(I x:v)std::cout<<x<<' ';std::cout<<'\n';};dfs(0);
}

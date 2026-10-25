// Enumerate integer v >= 0 with vv^T <= Q, including singular Q.
// Input maps free principal coordinates into range(Q); all tests exact.
#include <iostream>
#include <vector>
#include <functional>
using I=long long;using W=__int128_t;
// Exact floor(sqrt(a)) for every nonnegative signed-64-bit input.
// The midpoint avoids signed overflow; its square fits in signed __int128.
I root(I a){I l=0,h=a;while(l<h){I gap=h-l;I m=l+gap/2+gap%2;if(W(m)*m<=a)l=m;else h=m-1;}return l;}
int main(){int n,r;if(!(std::cin>>n>>r)||n<1||n>6||r<1||r>n)return 2;
 std::vector<std::vector<I>>Q(n,std::vector<I>(n)),A(r,std::vector<I>(r)),M(n,std::vector<I>(r));std::vector<int>ix(r);I det;
 for(auto&v:Q)for(I&x:v)std::cin>>x;for(int&i:ix)std::cin>>i;for(auto&v:A)for(I&x:v)std::cin>>x;std::cin>>det;for(auto&v:M)for(I&x:v)std::cin>>x;
 if(det<=0)return 2;std::vector<I>w(r),v(n),bound(r);for(int j=0;j<r;++j)bound[j]=root(Q[ix[j]][ix[j]]);
 std::function<void(int)>dfs=[&](int l){if(l<r){for(w[l]=0;w[l]<=bound[l];++w[l])dfs(l+1);return;}
  W z=0;for(int i=0;i<r;++i)for(int j=0;j<r;++j)z+=W(w[i])*A[i][j]*w[j];if(z>det)return;
  bool nz=false;for(int i=0;i<n;++i){z=0;for(int j=0;j<r;++j)z+=W(M[i][j])*w[j];if(z<0||z%det)return;z/=det;if(z>root(Q[i][i]))return;v[i]=(I)z;nz|=v[i]!=0;}if(!nz)return;
  for(int i=0;i<n;++i)for(int j=i;j<n;++j)if(W(v[i])*v[j]>Q[i][j])return;for(I x:v)std::cout<<x<<' ';std::cout<<'\n';};dfs(0);
}

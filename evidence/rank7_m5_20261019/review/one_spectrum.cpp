// Integer-only discovery of Theorem 6.8, arXiv:2203.06522v5.
// Output indices are zero-based (i0,i1,...,i9); Python rechecks them.
#include <array>
#include <iostream>
#include <vector>
using T=std::array<int,3>;
int N[8][8][8],du[8],mask[8][8],D[8][8][8][8];
int main(){int count,n;std::cin>>count;
 for(int row=0;row<count;++row){std::cin>>n;if(n<1||n>8)return 2;
  for(int i=0;i<n;++i)for(int j=0;j<n;++j){mask[i][j]=0;
   for(int k=0;k<n;++k){std::cin>>N[i][j][k];if(N[i][j][k])mask[i][j]|=1<<k;}
   if(N[i][j][0])du[i]=j;}
  for(int a=0;a<n;++a)for(int b=0;b<n;++b)for(int c=0;c<n;++c)for(int d=0;d<n;++d){
   D[a][b][c][d]=0;for(int k=0;k<n;++k)D[a][b][c][d]+=N[a][b][k]*N[c][d][k];}
  bool found=false;int out[10];
  for(int a=0;a<n&&!found;++a)for(int b=0;b<n&&!found;++b)for(int c=0;c<n&&!found;++c){
   if(N[b][a][c])continue;
   std::vector<T>L,R;
   for(int u=0;u<n;++u)for(int v=0;v<n;++v)for(int w=0;w<n;++w){
    if(N[u][a][w]&&N[v][u][b]&&N[v][w][c])L.push_back({u,v,w});
    if(N[u][w][a]&&N[b][u][v]&&N[v][w][c])R.push_back({u,v,w});}
   for(auto l:L){if(found)break;int u=l[0],v=l[1],w=l[2];
    for(auto r:R){int x=r[0],y=r[1],z=r[2];
     unsigned m=mask[u][x]&mask[du[v]][y]&mask[w][du[z]];
     if(!m||(m&(m-1)))continue;int p=__builtin_ctz(m);
     if(N[u][x][p]!=1||N[du[v]][y][p]!=1||N[w][du[z]][p]!=1)continue;
     if(!(D[v][p][b][x]==1||D[v][u][y][du[x]]==1||D[b][du[u]][y][du[p]]==1))continue;
     if(!(D[v][w][y][z]==1||D[v][p][c][du[z]]==1||D[y][du[p]][c][du[w]]==1))continue;
     if(!(D[u][a][p][z]==1||D[u][x][w][du[z]]==1||D[p][du[x]][w][du[a]]==1))continue;
     int ans[10]={p,a,b,c,u,v,w,x,y,z};for(int j=0;j<10;++j)out[j]=ans[j];found=true;break;
    }
   }
  }
  std::cout<<row<<' '<<found;if(found)for(int a:out)std::cout<<' '<<a;std::cout<<'\n';
 }
}

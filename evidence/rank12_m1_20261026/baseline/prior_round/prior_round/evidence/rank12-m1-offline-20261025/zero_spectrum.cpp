// Exact application of LPR (2022), Theorem 2.14. No field or pivotal assumption.
#include <iostream>
#include <vector>
#include <array>
using T=std::array<int,3>;
int N[12][12][12],d[12],mask[12][12];
int dot(int a,int b,int c,int e,int n){int s=0;for(int k=0;k<n;++k)s+=N[a][b][k]*N[c][e][k];return s;}
int main(){int count,n;std::cin>>count;for(int r=0;r<count;++r){std::cin>>n;if(n>12)return 2;for(int i=0;i<n;++i)for(int j=0;j<n;++j){mask[i][j]=0;for(int k=0;k<n;++k){std::cin>>N[i][j][k];if(N[i][j][k])mask[i][j]|=1<<k;}if(N[i][j][0])d[i]=j;}
 bool found=false;int out[9];
 for(int a=0;a<n&&!found;++a)for(int b=0;b<n&&!found;++b)for(int c=0;c<n&&!found;++c){if(N[b][a][c]!=1)continue;std::vector<T>L,R;
  for(int u=0;u<n;++u)for(int v=0;v<n;++v)for(int w=0;w<n;++w){
   if(N[u][a][w]&&N[v][u][b]&&N[v][w][c]&&(dot(v,u,c,d[a],n)==1||dot(b,d[u],c,d[w],n)==1||dot(d[v],b,w,d[a],n)==1))L.push_back({u,v,w});
   if(N[u][w][a]&&N[b][u][v]&&N[v][w][c]&&(dot(b,u,c,d[w],n)==1||dot(v,d[u],c,d[a],n)==1||dot(d[b],v,a,d[w],n)==1))R.push_back({u,v,w});
  }
  for(auto l:L){if(found)break;for(auto rr:R)if(!(mask[l[0]][rr[0]]&mask[d[l[1]]][rr[1]]&mask[l[2]][d[rr[2]]])){int z[9]={a,b,c,l[0],l[1],l[2],rr[0],rr[1],rr[2]};for(int i=0;i<9;++i)out[i]=z[i];found=true;break;}}
 }
 std::cout<<r<<' '<<found;if(found)for(int x:out)std::cout<<' '<<x;std::cout<<'\n';std::cout.flush();}
}

// Exact finite search for LPRV one-spectrum equations (6.13)--(6.18).
#include <iostream>
int N[8][8][8],du[8],D[8][8][8][8];
int main(){int count;std::cin>>count;for(int row=0;row<count;++row){int n;std::cin>>n;if(n<1||n>8)return 2;for(int i=0;i<n;++i)for(int j=0;j<n;++j)for(int k=0;k<n;++k){std::cin>>N[i][j][k];if(k==0&&N[i][j][k])du[i]=j;}for(int a=0;a<n;++a)for(int b=0;b<n;++b)for(int c=0;c<n;++c)for(int d=0;d<n;++d){D[a][b][c][d]=0;for(int k=0;k<n;++k)D[a][b][c][d]+=N[a][b][k]*N[c][d][k];}
bool found=false;int ans[10];
for(int u=0;u<n&&!found;++u)for(int x=0;x<n&&!found;++x)for(int v=0;v<n&&!found;++v)for(int y=0;y<n&&!found;++y)for(int w=0;w<n&&!found;++w)for(int z=0;z<n&&!found;++z){int sum=0,q=-1;for(int k=0;k<n;++k){int t=N[u][x][k]*N[du[v]][y][k]*N[w][du[z]][k];sum+=t;if(t)q=k;}if(sum!=1)continue;
for(int a=0;a<n&&!found;++a){if(!N[u][a][w]||!N[x][z][a])continue;if(D[u][x][w][du[z]]!=1&&D[u][a][q][z]!=1&&D[q][du[x]][w][du[a]]!=1)continue;
for(int b=0;b<n&&!found;++b){if(!N[v][u][b]||!N[b][x][y])continue;if(D[v][u][y][du[x]]!=1&&D[v][q][b][x]!=1&&D[b][du[u]][y][du[q]]!=1)continue;
for(int c=0;c<n&&!found;++c){if(N[b][a][c]||!N[v][w][c]||!N[y][z][c])continue;if(D[v][q][c][du[z]]!=1&&D[v][w][y][z]!=1&&D[y][du[q]][c][du[w]]!=1)continue;int tmp[10]={q,a,b,c,u,v,w,x,y,z};for(int i=0;i<10;++i)ans[i]=tmp[i];found=true;}}}}
std::cout<<row<<' '<<found;if(found)for(int a:ans)std::cout<<' '<<a;std::cout<<'\n';std::cout.flush();}}

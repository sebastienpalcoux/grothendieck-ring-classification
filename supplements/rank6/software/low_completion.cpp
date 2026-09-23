// Exact low-induction row-sum join, retaining every nonnegative PSD remainder.
#include <array>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <iostream>
#include <tuple>
using V=std::array<int,4>;using W=__int128;using Pair=std::pair<int,int>;
struct Hash{size_t operator()(const V&v)const{size_t h=0;for(int a:v)h=h*1000003+(unsigned)a;return h;}};
std::array<std::vector<V>,4>c;long long B[4][4];V target;bool same[4][4];
bool good(const std::array<int,4>&z){
 for(int i=0;i<4;i++)for(int j=i+1;j<4;j++)if(same[i][j]&&c[i][z[i]]>c[j][z[j]])return false;
 long long Q[4][4];for(int i=0;i<4;i++)for(int j=i;j<4;j++){
  Q[i][j]=B[i][j];for(int k=0;k<4;k++)Q[i][j]-=(long long)c[k][z[k]][i]*c[k][z[k]][j];
  if(Q[i][j]<0)return false;Q[j][i]=Q[i][j];
 }
 for(int i=0;i<4;i++)for(int j=i+1;j<4;j++)if((W)Q[i][i]*Q[j][j]<(W)Q[i][j]*Q[i][j])return false;
 for(int i=0;i<4;i++)for(int j=i+1;j<4;j++)for(int k=j+1;k<4;k++){
  W d=(W)Q[i][i]*(Q[j][j]*Q[k][k]-Q[j][k]*Q[k][j])-(W)Q[i][j]*(Q[j][i]*Q[k][k]-Q[j][k]*Q[k][i])+(W)Q[i][k]*(Q[j][i]*Q[k][j]-Q[j][j]*Q[k][i]);if(d<0)return false;
 }
 std::array<int,4>p{0,1,2,3};W det=0;do{int parity=0;W x=1;for(int i=0;i<4;i++){x*=Q[i][p[i]];for(int j=i+1;j<4;j++)parity^=(p[i]>p[j]);}det+=parity?-x:x;}while(std::next_permutation(p.begin(),p.end()));return det>=0;
}
int main(){
 for(int&v:target)if(!(std::cin>>v))return 2;
 for(auto&row:B)for(auto&v:row)std::cin>>v;
 for(auto&list:c){int n;std::cin>>n;list.resize(n);for(auto&v:list)for(int&x:v)std::cin>>x;}
 for(int i=0;i<4;i++)for(int j=0;j<4;j++)same[i][j]=(c[i]==c[j]);
 std::array<std::array<int,4>,3>part{{{0,1,2,3},{0,2,1,3},{0,3,1,2}}};
 auto cost=[&](const auto&p){return c[p[0]].size()*c[p[1]].size()+c[p[2]].size()*c[p[3]].size();};
 auto p=*std::min_element(part.begin(),part.end(),[&](auto&a,auto&b){return cost(a)<cost(b);});
 if(c[p[0]].size()*c[p[1]].size()>c[p[2]].size()*c[p[3]].size()){std::swap(p[0],p[2]);std::swap(p[1],p[3]);}
 std::unordered_map<V,std::vector<Pair>,Hash>join;
 for(int a=0;a<(int)c[p[0]].size();a++)for(int b=0;b<(int)c[p[1]].size();b++){
  if(same[p[0]][p[1]]&&c[p[0]][a]>c[p[1]][b])continue;
  V key;bool ok=true;for(int i=0;i<4;i++){key[i]=c[p[0]][a][i]+c[p[1]][b][i];if(key[i]>target[i])ok=false;}
  if(ok)join[key].push_back({a,b});
 }
 for(int a=0;a<(int)c[p[2]].size();a++)for(int b=0;b<(int)c[p[3]].size();b++){
  if(same[p[2]][p[3]]&&c[p[2]][a]>c[p[3]][b])continue;
  V key;for(int i=0;i<4;i++)key[i]=target[i]-c[p[2]][a][i]-c[p[3]][b][i];auto it=join.find(key);if(it==join.end())continue;
  for(auto pair:it->second){std::array<int,4>z;z[p[0]]=pair.first;z[p[1]]=pair.second;z[p[2]]=a;z[p[3]]=b;if(good(z))std::cout<<z[0]<<' '<<z[1]<<' '<<z[2]<<' '<<z[3]<<'\n';}
 }
}

#include <iostream>
#include <vector>
#include <cmath>
using namespace std;
int n,k,den,ns;vector<int> bounds,solved,freec,b,z,x;vector<vector<int>> E,H,G;long long leaves=0,modpass=0,count=0;
void rec(int l){
 if(l<(int)freec.size()){int p=freec[l];for(z[p]=0;z[p]<=bounds[p];++z[p])rec(l+1);return;}
 ++leaves;
 for(int q=0;q<ns;++q){long long v=E[q][k];for(int p:freec)v-=E[q][p]*z[p];v=(v%den+den)%den;if(v>bounds[solved[q]])return;z[solved[q]]=v;}
 ++modpass;
 for(int i=0;i<n;++i){long long v=b[i];for(int j=0;j<k;++j)v+=H[i][j]*z[j];if(v<0||v%den)return;x[i]=v/den;if(x[i]*x[i]>G[i][i])return;}
 for(int i=0;i<n;++i)if(x[i])for(int j=i;j<n;++j)if(x[i]*x[j]>G[i][j])return;
 for(int i=0;i<n;++i)cout<<x[i]<<(i+1==n?'\n':' ');++count;
}
int main(){cin>>n>>k>>den>>ns;bounds.resize(k);solved.resize(ns);freec.resize(k-ns);b.resize(n);z.resize(k);x.resize(n);for(auto&v:bounds)cin>>v;for(auto&v:solved)cin>>v;for(auto&v:freec)cin>>v;for(auto&v:b)cin>>v;E.assign(ns,vector<int>(k+1));H.assign(n,vector<int>(k));G.assign(n,vector<int>(n));for(auto&r:E)for(auto&v:r)cin>>v;for(auto&r:H)for(auto&v:r)cin>>v;for(auto&r:G)for(auto&v:r)cin>>v;rec(0);cerr<<"leaves "<<leaves<<" modpass "<<modpass<<" retained "<<count<<"\n";}

#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
using namespace std;
int n,m;vector<int> bd,ub,cs;vector<vector<int>> co,mn,mx;unsigned long long nodes=0,prof=0;bool complete=true;ofstream out;auto start=chrono::steady_clock::now();
void dfs(int l,vector<int>&p){
 if(!complete)return;++nodes;
 if(nodes%100000==0 && chrono::duration<double>(chrono::steady_clock::now()-start).count()>750){complete=false;return;}
 for(int i=0;i<m;++i)if(p[i]+mx[l][i]<0||p[i]+mn[l][i]>ub[i])return;
 if(l==n){if(prof>=200000){complete=false;return;}++prof;out<<'[';for(int i=0;i<m;++i){if(i)out<<',';out<<p[i];}out<<"]\n";return;}
 for(int x=0;x<=bd[l];++x){dfs(l+1,p);for(int i=0;i<m;++i)p[i]+=co[i][l];if(!complete)break;}
 // No caller reads p after a cancelled branch, but restore exactly otherwise.
 if(complete)for(int i=0;i<m;++i)p[i]-=co[i][l]*(bd[l]+1);
}
int main(int argc,char**argv){cin>>n>>m;bd.resize(n);ub.resize(m);cs.resize(m);co.assign(m,vector<int>(n));for(int &x:bd)cin>>x;for(int&x:ub)cin>>x;for(int&x:cs)cin>>x;for(auto&r:co)for(int&x:r)cin>>x;mn.assign(n+1,vector<int>(m));mx=mn;
 for(int l=n-1;l>=0;--l)for(int i=0;i<m;++i){int z=co[i][l]*bd[l];mn[l][i]=mn[l+1][i]+min(0,z);mx[l][i]=mx[l+1][i]+max(0,z);}out.open(argv[1]);dfs(0,cs);out.close();cout<<"{\"complete\":"<<(complete?"true":"false")<<",\"nodes\":"<<nodes<<",\"profiles\":"<<prof<<",\"cap\":200000}"<<endl;
}

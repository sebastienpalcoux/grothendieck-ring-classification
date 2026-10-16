#include <array>
#include <vector>
#include <iostream>
#include <cstdint>
using namespace std;
using Z=long long; using Poly=vector<Z>; using Mat=vector<vector<Z>>;
Z mod(Z a,Z p){a%=p;return a<0?a+p:a;}
Z powm(Z a,Z n,Z p){Z r=1;for(;n;n>>=1,a=a*a%p)if(n&1)r=r*a%p;return r;}
void trim(Poly&a){while(!a.empty()&&!a.back())a.pop_back();}
Poly rem(Poly a,Poly b,Z p){trim(a);trim(b);Z inv=powm(b.back(),p-2,p);while(a.size()>=b.size()){Z c=a.back()*inv%p;int sh=a.size()-b.size();for(int i=0;i<(int)b.size();i++)a[i+sh]=mod(a[i+sh]-c*b[i],p);trim(a);}return a;}
Poly gcdp(Poly a,Poly b,Z p){trim(a);trim(b);while(!b.empty()){Poly c=rem(a,b,p);a=b;b=c;}return a;}
Poly cp(Mat A,Z p){int n=A.size();Mat B(n,vector<Z>(n));for(int i=0;i<n;i++)B[i][i]=1;Poly c(n+1);c[n]=1;for(int k=1;k<=n;k++){Mat D(n,vector<Z>(n));for(int i=0;i<n;i++)for(int j=0;j<n;j++)for(int l=0;l<n;l++)D[i][j]=mod(D[i][j]+A[i][l]*B[l][j],p);Z tr=0;for(int i=0;i<n;i++)tr+=D[i][i];Z v=mod(-tr*powm(k,p-2,p),p);c[n-k]=v;for(int i=0;i<n;i++)D[i][i]=mod(D[i][i]+v,p);B=D;}return c;}
bool possible(Mat A,Z p){Poly f=cp(A,p);Mat B(5,vector<Z>(5));for(int i=0;i<5;i++)for(int j=0;j<5;j++)B[i][j]=A[i+1][j+1];Poly q=cp(B,p),dp(6);for(int i=1;i<=6;i++)dp[i-1]=mod(2*i*f[i],p);
 for(int d: {180,360}){Poly g(6);for(int i=0;i<6;i++)g[i]=mod(dp[i]-d*q[i],p);if(gcdp(f,g,p).size()>1)return true;}
 for(int a:{270,450}){Poly g(11);for(int i=0;i<6;i++)for(int j=0;j<6;j++)g[i+j]=mod(g[i+j]+mod(dp[i]-a*q[i],p)*mod(dp[j]-a*q[j],p)-40500*q[i]*q[j],p);if(gcdp(f,g,p).size()>1)return true;}
 return false;
}
vector<vector<int>> ds;vector<pair<int,int>> ix;vector<int> cs;Z total=0,pass1=0,pass2=0;
void walk(int k,Mat&A){if(k==(int)ds.size()){total++;if(!possible(A,1009))return;pass1++;if(!possible(A,1013))return;pass2++;for(int c:cs)cout<<c<<' ';cout<<'\n';return;}auto [i,j]=ix[k];for(int c:ds[k]){cs[k]=c;A[i][j]=A[j][i]=c;walk(k+1,A);}}
int main(){int n;cin>>n;ds.resize(n);ix.resize(n);cs.resize(n);for(int k=0;k<n;k++){int i,j,z;cin>>i>>j>>z;ix[k]={i,j};ds[k].resize(z);for(int&a:ds[k])cin>>a;}Mat A(6,vector<Z>(6));A[0][1]=1;A[1][0]=2;walk(0,A);cerr<<"total "<<total<<" pass1009 "<<pass1<<" pass1013 "<<pass2<<'\n';}

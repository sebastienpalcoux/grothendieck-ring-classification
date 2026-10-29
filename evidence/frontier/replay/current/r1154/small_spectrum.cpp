#include <iostream>
#include <vector>
#include <array>
using namespace std;
int main(){int n;cin>>n;int N[10][10][10]={},du[10]={};for(int i=0;i<n;i++)for(int j=0;j<n;j++)for(int k=0;k<n;k++)cin>>N[i][j][k];for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(N[i][j][0])du[i]=j;
int dot[10][10][10][10]={};for(int a=0;a<n;a++)for(int b=0;b<n;b++)for(int c=0;c<n;c++)for(int d=0;d<n;d++)for(int k=0;k<n;k++)dot[a][b][c][d]+=N[a][b][k]*N[c][d][k];
long long tested=0;
for(int i1=0;i1<n;i1++)for(int i2=0;i2<n;i2++)for(int i3=0;i3<n;i3++){int lhs=N[i2][i1][i3];if(lhs>1)continue;
for(int i4=0;i4<n;i4++)for(int i5=0;i5<n;i5++){if(!N[i5][i4][i2])continue;for(int i6=0;i6<n;i6++){if(!N[i4][i1][i6]||!N[i5][i6][i3])continue;
for(int i7=0;i7<n;i7++)for(int i8=0;i8<n;i8++){if(!N[i2][i7][i8])continue;for(int i9=0;i9<n;i9++){if(!N[i7][i9][i1]||!N[i8][i9][i3])continue;tested++;
int sp=0,i0=-1;for(int k=0;k<n;k++){int z=N[i4][i7][k]*N[du[i5]][i8][k]*N[i6][du[i9]][k];sp+=z;if(z)i0=k;}
bool bad=false;
if(lhs==1&&sp==0)bad=(dot[i5][i6][i2][i1]==1||dot[i5][i4][i3][du[i1]]==1||dot[i2][du[i4]][i3][du[i6]]==1)&&(dot[i2][i1][i8][i9]==1||dot[i2][i7][i3][du[i9]]==1||dot[i8][du[i7]][i3][du[i1]]==1);
if(lhs==0&&sp==1)bad=(dot[i5][i0][i2][i7]==1||dot[i5][i4][i8][du[i7]]==1||dot[i2][du[i4]][i8][du[i0]]==1)&&(dot[i5][i6][i8][i9]==1||dot[i5][i0][i3][du[i9]]==1||dot[i8][du[i0]][i3][du[i6]]==1)&&(dot[i4][i1][i0][i9]==1||dot[i4][i7][i6][du[i9]]==1||dot[i0][du[i7]][i6][du[i1]]==1);
if(bad){cout<<"EXCLUDED spectrum="<<sp<<" indices="<<i0<<","<<i1<<","<<i2<<","<<i3<<","<<i4<<","<<i5<<","<<i6<<","<<i7<<","<<i8<<","<<i9<<"\n";return 0;}
}}}}}
cout<<"No zero/one spectrum witness; eligible configurations="<<tested<<"\n";}

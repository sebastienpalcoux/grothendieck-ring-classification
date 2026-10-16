#include <array>
#include <iostream>
#include <algorithm>
using I=long long;using P=std::array<I,10>;
bool valid(const P&p){auto[a,b,c,d,e,f,g,h,i,j]=p;return a*d-b*b+b*g+c*h-d*d-e*e+1==0&&a*e-b*c+b*h+c*i-d*e-e*f==0&&b*e-c*d+d*h-e*g+e*i-f*h==0&&a*f+b*i-c*c+c*j-e*e-f*f+1==0&&b*f-c*e+d*i-e*h+e*j-f*i==0&&d*f-e*e+g*i-h*h+h*j-i*i+1==0;}
int main(int argc,char**argv){int M=std::stoi(argv[1]);P p;p.fill(-M);while(true){if(valid(p)){std::cout<<"S";for(I v:p)std::cout<<' '<<v;std::cout<<'\n';}int k=9;while(k>=0&&p[k]==M){p[k]=-M;--k;}if(k<0)break;++p[k];}}

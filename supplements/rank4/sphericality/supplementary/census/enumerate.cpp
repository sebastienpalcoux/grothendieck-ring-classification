// Enumerate all ordinary rank-four fusion rings with bounded multiplicities.
// The row loop solves scalar equations k*x = r in [0,M]. Every free
// variable is traversed if k=r=0. The independent Python pass checks
// associativity, isomorphism classes and all strict dimension bounds again.
#include <algorithm>
#include <array>
#include <iostream>
#include <stdexcept>
#include <string>
using I = long long;
using P = std::array<I,10>;
using Mat = std::array<std::array<I,4>,4>;
using Tensor = std::array<Mat,4>;
const Mat unit = {{{1,0,0,0},{0,1,0,0},{0,0,1,0},{0,0,0,1}}};

struct Range {
    I first, last;
};
Range solve(I k, I rhs, I upper) {
    if (!k) return {0, rhs == 0 ? upper : -1};
    if (rhs < 0 || rhs > k*upper || rhs % k) return {0,-1};
    return {rhs/k,rhs/k};
}
Tensor sd_tensor(const P& p) {
    auto [a,b,c,d,e,f,g,h,i,j] = p;
    return {unit, Mat{{{0,1,0,0},{1,a,b,c},{0,b,d,e},{0,c,e,f}}},
            Mat{{{0,0,1,0},{0,b,d,e},{1,d,g,h},{0,e,h,i}}},
            Mat{{{0,0,0,1},{0,c,e,f},{0,e,h,i},{1,f,i,j}}}};
}
Tensor ns_tensor(I a,I b,I c,I d,I e,I f) {
    return {unit, Mat{{{0,1,0,0},{1,a,b,b},{0,b,c,d},{0,b,d,c}}},
            Mat{{{0,0,1,0},{0,b,c,d},{0,d,e,f},{1,c,e,e}}},
            Mat{{{0,0,0,1},{0,b,d,c},{1,c,e,e},{0,d,f,e}}}};
}
bool bounded(const Tensor& R, I limit) {
    __int128_t q[4][4]{},previous=1;
    for(int i=0;i<4;i++) for(int j=0;j<4;j++){
        q[i][j]=i==j ? limit : 0;
        for(const Mat& n:R) for(int k=0;k<4;k++) q[i][j]-=n[i][k]*n[j][k];
    }
    for(int k=0;k<4;k++){
        auto pivot=q[k][k];
        if (pivot<=0) return false;
        for(int i=k+1;i<4;i++) for(int j=k+1;j<4;j++){
            auto numerator=q[i][j]*pivot-q[i][k]*q[k][j];
            if(numerator%previous) throw std::logic_error("nonexact determinant division");
            q[i][j]=numerator/previous;
        }
        previous=pivot;
    }
    return true;
}
bool canonical(const P& p,const Tensor& r) {
    std::array<int,3> order{1,2,3};
    do {
        P image{}; int pos=0;
        for(int i=0;i<3;i++)for(int j=i;j<3;j++)for(int k=j;k<3;k++)
            image[pos++]=r[order[i]][order[j]][order[k]];
        if(image[1]==p[1] && image<p) return false;
    }while(std::next_permutation(order.begin(),order.end()));
    return true;
}
void self_dual(I M,I D,bool unpruned) {
    for(I b=0;b<=M;b++)for(I c=b;c<=M;c++)for(I d=b;d<=M;d++)
    for(I e=0;e<=M;e++)for(I f=b;f<=M;f++)for(I a=0;a<=M;a++){
        if(!unpruned && 2+2*b*b+2*c*c+d*d+2*e*e+f*f+a*a>=D) continue;
        for(I h=b;h<=M;h++){
            auto gs=solve(b,b*b+d*d+e*e-1-a*d-c*h,M);
            if(gs.first>gs.last) continue;
            auto is=solve(c,b*c+e*(d+f-a)-b*h,M);
            for(I i=std::max(b,is.first);i<=is.last;i++){
                auto js=solve(c,c*c+e*e+f*f-1-a*f-b*i,M);
                if(js.first>js.last) continue;
                for(I g=gs.first;g<=gs.last;g++){
                    if(b*e-c*d+d*h-e*g+e*i-f*h) continue;
                    for(I j=js.first;j<=js.last;j++){
                        if(b*f-c*e+d*i-e*h+e*j-f*i ||
                           d*f-e*e+g*i-h*h+h*j-i*i+1) continue;
                        P p{a,b,c,d,e,f,g,h,i,j}; auto r=sd_tensor(p);
                        if(canonical(p,r) && (unpruned || bounded(r,D))){
                            std::cout<<"S"; for(auto k:p)std::cout<<' '<<k; std::cout<<'\n';
                        }
                    }
                }
            }
        }
    }
}
void dual_pair(I M,I D,bool unpruned) {
    for(I c=0;c<=M;c++)for(I d=0;d<=M;d++)for(I e=0;e<=M;e++)
    for(I f=0;f<=M;f++){
        if(-c*c+d*d-e*e+f*f-1) continue;
        for(I b=0;b<=M;b++){
            if(b*(c-d)+d*(e-f)) continue;
            auto as=solve(c,b*b-2*b*e+c*c+d*d-1,M);
            for(I a=as.first;a<=as.last;a++){
                if(a*d-b*b+b*e+b*f-2*c*d) continue;
                if(unpruned || bounded(ns_tensor(a,b,c,d,e,f),D))
                    std::cout<<"N "<<a<<' '<<b<<' '<<c<<' '<<d<<' '<<e<<' '<<f<<'\n';
            }
        }
    }
}
int main(int argc,char** argv) {
    if(argc<3 || argc>4) throw std::invalid_argument("usage: enumerate M D [--unpruned]");
    I M=std::stoll(argv[1]),D=std::stoll(argv[2]);
    if(M<1 || M>31 || D<5 || D>1000) throw std::invalid_argument("require 1 <= M <= 31 and 5 <= D <= 1000");
    bool unpruned=argc==4;
    if(unpruned && std::string(argv[3])!="--unpruned") throw std::invalid_argument("unknown option");
    self_dual(M,D,unpruned);dual_pair(M,D,unpruned);
}

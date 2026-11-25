#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
using I = int64_t;
using W = __int128_t;

// All intervals use the common denominator Q. G is the denominator of the
// rational supporting directions. A coordinate box always encloses the exact
// feasible region, including points on a subdivision plane.
constexpr I Q = 1LL << 21, G = 1LL << 15;
constexpr int ND = 12;
struct Interval { I lo, hi; };
using Box = std::array<Interval,12>;
using Row = std::array<I,6>;
I ceil_nonnegative(I a,I b){return (a+b-1)/b;}
I ceiling_ratio(W a,W b){return I((a+b-1)/b);}
I sqrt_floor(I n){
    I h=1;while(h*h<=n)h*=2;
    I l=h/2;
    while(h-l>1){I m=(h+l)/2;if(m*m<=n)l=m;else h=m;}
    return l;
}
I sqrt_upper(I n){return sqrt_floor(std::max<I>(0,n))+1;}
constexpr std::array<int,3> cs={56,7,8};
std::array<I,3> pcaps,qcaps,sqrtC;
std::array<std::array<Row,ND>,3> directions;
I eps_grid;
uint64_t nodes=0, pruned=0;
I max_pruned=0, max_depth=0;
I dot_lower(const Interval* x,const Row& c){
    I value=0;
    for(int i=0;i<6;i++)value+=c[i]*(c[i]<0?x[i].hi:x[i].lo);
    return value;
}
bool contract(Interval* x,const Row& c,I rhs){
    I slack=rhs-dot_lower(x,c);
    if(slack<0)return false;
    for(int i=0;i<6;i++){
        if(c[i]>0)x[i].hi=std::min(x[i].hi,x[i].lo+ceil_nonnegative(slack,c[i]));
        else if(c[i]<0)x[i].lo=std::max(x[i].lo,x[i].hi-ceil_nonnegative(slack,-c[i]));
    }
    return true;
}
bool narrow(Box& x){
    static constexpr Row pos={1,1,1,1,1,1},neg={-1,-1,-1,-1,-1,-1};
    for(int pass=0;pass<2;pass++){
        for(int start:{0,6}){
            if(!contract(x.data()+start,pos,Q)||!contract(x.data()+start,neg,-Q))return false;
        }
        for(int k=0;k<3;k++){
            I lp=0,lq=0,c=cs[k];
            for(const Row& r:directions[k]){
                lp=std::max(lp,dot_lower(x.data(),r)/G);
                lq=std::max(lq,dot_lower(x.data()+6,r)/G);
            }
            if(lp>pcaps[k]||lq>qcaps[k]||sqrtC[k]*lq+c*lp*lp>2*Q*Q)return false;
            I pu=std::min(pcaps[k],sqrt_upper((2*Q*Q-sqrtC[k]*lq)/c));
            I qu=std::min(qcaps[k],ceil_nonnegative(2*Q*Q-c*lp*lp,sqrtC[k]));
            for(const Row& r:directions[k]){
                if(!contract(x.data(),r,G*pu)||!contract(x.data()+6,r,G*qu))return false;
            }
        }
    }
    return true;
}
struct Halfspace {I a,b,c;};
I moment_upper(const Box& x){
    auto pu=[&](int i){return x[i].hi;};
    auto ql=[&](int i){return x[6+i].lo;};
    I p4=pu(4),p2=pu(2), upper=p2+p4;
    std::array<Halfspace,20> h;
    int n=0;
    // a=p0/q0, v=p0/q2. Always 0<=v<=a<=1.
    h[n++]={Q*Q,0,Q*Q}; h[n++]={-Q*Q,Q*Q,0};
    h[n++]={-Q*Q,0,0}; h[n++]={0,-Q*Q,0};
    for(int i=1;i<6;i++){
        // Galois spectral comparisons a*q_i<=p_i and v*q_(i+2)<=p_i.
        h[n++]={Q*ql(i),0,Q*pu(i)};
        h[n++]={0,Q*ql((i+2)%6),Q*pu(i)};
        I error=0;
        for(int l=1;l<6;l++)error+=ceil_nonnegative(pu((i+l)%6)*pu((i+l)%6),x[l].lo);
        // Multiply the ordinary/signed comparison of second moments by p0.
        h[n++]={ql(i)*ql(i),ql((i+2)%6)*ql((i+2)%6),pu(i)*pu(i)+pu(0)*error};
    }
    // Every nonnegative combination majorizing (p4,p2) gives an upper
    // bound on p4*a+p2*v. Test exact two-row combinations giving equality.
    for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){
        W de=W(h[i].a)*h[j].b-W(h[i].b)*h[j].a;
        if(de==0)continue;
        W wi=W(p4)*h[j].b-W(p2)*h[j].a, wj=W(p2)*h[i].a-W(p4)*h[i].b;
        if(de<0){de=-de;wi=-wi;wj=-wj;}
        if(wi<0||wj<0)continue;
        W num=wi*h[i].c+wj*h[j].c;
        if(num<W(upper)*de)upper=ceiling_ratio(num,de);
    }
    for(int i:{1,3,4,5})upper+=ceil_nonnegative(pu(i)*pu((i+4)%6),ql(i));
    return upper;
}
bool exclude(Box x,int depth){
    nodes++; max_depth=std::max<I>(max_depth,depth);
    if(!narrow(x))return true;
    I upper=moment_upper(x);
    if(upper<Q){max_pruned=std::max(max_pruned,upper);pruned++;return true;}
    I score=0;int at=-1;
    for(int i=0;i<12;i++){
        if(i==0||i==6||i==8)continue;
        I width=x[i].hi-x[i].lo, s=width*(i<6?10:13);
        if(width>1&&s>score){at=i;score=s;}
    }
    if(at<0){
        std::cerr<<"Unresolved grid box at depth "<<depth<<", k upper "<<upper<<"/"<<Q<<"\n";
        for(auto const& y:x)std::cerr<<y.lo<<":"<<y.hi<<" ";
        std::cerr<<"\n";
        return false;
    }
    I mid=(x[at].lo+x[at].hi)/2; Box other=x;
    x[at].hi=mid; other[at].lo=mid;
    return exclude(x,depth+1)&&exclude(other,depth+1);
}
int main(int argc,char**argv){
    // The two larger frequency conductors for b=9 only strengthen the
    // inequalities. Check b=7 once, simultaneously for the two fields.
    I denom=argc>1?std::atoll(argv[1]):200;
    if(denom<100||denom>Q){std::cerr<<"Require 100 <= denominator <= "<<Q<<"\n";return 2;}
    eps_grid=ceil_nonnegative(Q,denom);
    I t=sqrt_floor(3*G*G/4);
    std::array<I,12> coslow={G,t,G/2,0,-G/2,-t-1,-G,-t-1,-G/2,0,G/2,t};
    for(int k=0;k<3;k++){
        I c=cs[k];sqrtC[k]=sqrt_floor(c*Q*Q);
        pcaps[k]=sqrt_upper(std::gcd<I>(c,2)*Q*Q/c);
        qcaps[k]=sqrt_upper(std::gcd<I>(c,4)*Q*Q/c);
        for(int j=0;j<ND;j++)for(int i=0;i<6;i++){
            int phase=(12+2*i*(k+1)-j)%12;
            directions[k][j][i]=coslow[phase];
        }
    }
    Box box;for(auto& u:box)u={Q/50,Q};
    box[0]=box[6]=box[8]={0,eps_grid};
    bool ok=exclude(box,0);
    std::cout<<(ok?"EXCLUDED":"UNRESOLVED")<<"; denominator="<<denom<<"; nodes="<<nodes
             <<"; moment_leaves="<<pruned<<"; greatest_leaf_upper="<<max_pruned
             <<"/"<<Q<<"; max_depth="<<max_depth<<"\n";
    return ok?0:1;
}

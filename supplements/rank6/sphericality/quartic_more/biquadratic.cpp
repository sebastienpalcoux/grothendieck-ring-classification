// Exact outer enumeration of primitive totally positive d-numbers in the
// bounded biquadratic fields of higher_degree_quartic_bounds_certificate.json.
// Input lines: a b c trace_cap; a,b,c are quadratic field discriminants.
// Output is a text certificate, not a categorical exclusion.
#include <cstdint>
#include <cmath>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using i64=std::int64_t;
using i128=__int128_t;

i64 isqrt(i64 n) {
    i64 r=static_cast<i64>(std::sqrt(static_cast<long double>(n)));
    while ((r+1)*(r+1)<=n) ++r;
    while (r*r>n) --r;
    return r;
}
bool square(i64 n) { if(n<0)return false; auto r=isqrt(n);return r*r==n; }
i128 fourth(i64 n) {i128 q=static_cast<i128>(n)*n;return q*q;}

int main(int argc,char** argv) {
    if(argc!=3) {std::cerr<<"usage: enumerator fields.txt candidates.txt\n";return 2;}
    std::ifstream input(argv[1]);std::ofstream output(argv[2]);
    if(!input||!output)return 2;
    i64 a,b,c,cap,fields=0,tuples=0,integral=0,tp=0,small=0,dnumbers=0;
    while(input>>a>>b>>c>>cap) {
        ++fields;
        const i64 k=isqrt(a*b*c);
        if(k*k!=a*b*c)return 3;
        const bool two_totally_ramified=(a%2==0&&b%2==0&&c%2==0);
        for(i64 A=5;A<=cap;++A) {
            const i64 A2=A*A,A3=A2*A,A4=A2*A2;
            const i64 U=isqrt((A2-1)/a),V=isqrt((A2-1)/b),W=isqrt((A2-1)/c);
            for(i64 u=0;u<=U;++u)for(i64 v=0;v<=V;++v) {
                i64 low=(u&&v)?-W:0;
                for(i64 w=low;w<=W;++w) {
                    if((u!=0)+(v!=0)+(w!=0)<2)continue;
                    ++tuples;
                    const i64 X=a*u*u,Y=b*v*v,Z=c*w*w,S=X+Y+Z,T=k*u*v*w;
                    const i64 B8=3*A2-S;
                    const i64 C16=A3-A*S+2*T;
                    const i64 N256=A4-2*S*A2+8*A*T+S*S-4*(X*Y+X*Z+Y*Z);
                    if(B8%8||C16%16||N256%256)continue;
                    ++integral;
                    const i64 B=B8/8,C=C16/16,N=N256/256;
                    // The four conjugates are real. Positive elementary
                    // symmetric coefficients are equivalent to positivity.
                    if(B<=0||C<=0||N<=0)continue;
                    ++tp;
                    // The same test on alpha-1 excludes all roots>1.
                    if(A-4>0&&B-3*A+6>0&&C-2*B+3*A-4>0&&N-C+B-A+1>0)continue;
                    ++small;
                    // A d-number in a V4 field has even odd-prime norm
                    // valuations; its norm is a square or twice a square.
                    if(!square(N)&&!(two_totally_ramified&&N%2==0&&square(N/2)))continue;
                    if(A4%N)continue;
                    const i128 N2=static_cast<i128>(N)*N,N3=N2*N;
                    if(fourth(B)%N2||fourth(C)%N3)continue;
                    ++dnumbers;
                    output<<a<<' '<<b<<' '<<c<<' '<<A<<' '<<u<<' '<<v<<' '<<w
                          <<' '<<B<<' '<<C<<' '<<N<<'\n';
                }
            }
        }
    }
    std::cout<<"fields "<<fields<<"\ncanonical_primitive_tuples "<<tuples
             <<"\nintegral "<<integral<<"\ntotally_positive "<<tp
             <<"\nminimum_below_one "<<small<<"\ndnumbers "<<dnumbers<<"\n";
}

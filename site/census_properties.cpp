// Exact structural flags for the published census. This is an index builder,
// not an enumeration or categorification test. See FULL_CENSUS.md for proofs.
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>
#include <boost/multiprecision/cpp_int.hpp>
using boost::multiprecision::cpp_int;
using I = __int128_t;
using Matrix = std::vector<std::vector<long long>>;

static void u16(std::ostream& out, unsigned value) {
    out.put(char(value & 255)); out.put(char(value >> 8));
}

// Exact fraction-free symmetric elimination. Positive pivots and zero rows
// characterize positive semidefiniteness; a zero pivot also proves singularity.
static bool psd_singular(const Matrix& a, long long eigenvalue) {
    int n = int(a.size());
    std::vector<std::vector<cpp_int>> b(n, std::vector<cpp_int>(n));
    for (int i=0;i<n;i++) for (int j=0;j<n;j++)
        b[i][j] = (i == j ? cpp_int(eigenvalue) : cpp_int(0)) - a[i][j];
    cpp_int previous = 1;
    bool singular = false;
    for (int k=0;k<n;k++) {
        cpp_int pivot = b[k][k];
        if (pivot < 0) return false;
        if (pivot == 0) {
            for (int j=k+1;j<n;j++) if (b[k][j] != 0) return false;
            singular = true;
            continue;
        }
        for (int i=k+1;i<n;i++) for (int j=i;j<n;j++) {
            cpp_int numerator = pivot*b[i][j]-b[i][k]*b[k][j];
            if (numerator % previous != 0) throw std::runtime_error("Nonexact Bareiss division");
            b[i][j] = numerator / previous;
            b[j][i] = b[i][j];
        }
        previous = pivot;
    }
    return singular;
}

// Collatz bounds require only v>0. Rounding a floating vector merely proposes
// a rational test vector; every conclusion below uses integer arithmetic.
template<class Integer>
static std::pair<long long,long long> integer_bounds(const Matrix& a,
                                                    const std::vector<Integer>& v) {
    long long low = std::numeric_limits<long long>::max(), high = 0;
    for (size_t j=0;j<v.size();j++) {
        Integer numerator = 0;
        for (size_t k=0;k<v.size();k++) numerator += a[j][k]*v[k];
        Integer floor = numerator/v[j], ceil = (numerator+v[j]-1)/v[j];
        long long f, c;
        if constexpr (std::is_same_v<Integer,cpp_int>) {
            f=floor.template convert_to<long long>(); c=ceil.template convert_to<long long>();
        } else { f=static_cast<long long>(floor); c=static_cast<long long>(ceil); }
        low=std::min(low,c); high=std::max(high,f);
    }
    return {low,high};
}

static bool dimension_character(const std::vector<int>& t, int n,
                                const std::vector<long long>& d) {
    if (d[0] != 1 || *std::min_element(d.begin(),d.end()) < 1) return false;
    for (int i=0;i<n;i++) for (int j=0;j<n;j++) {
        I sum=0;
        for (int k=0;k<n;k++) sum += I(t[(i*n+j)*n+k])*d[k];
        if (sum != I(d[i])*d[j]) return false;
    }
    return true;
}

// -1 denotes an undecided bound, never a negative property value.
template<class Integer>
static std::pair<int,int> dimension_flags(const std::vector<int>& t, int n,
                                         const std::vector<Matrix>& matrices,
                                         const Matrix& omega,
                                         const std::vector<Integer>& v,
                                         int integral=-1, int weak=-1) {
    if (integral < 0) {
        bool unique=true; std::vector<long long> candidate(n);
        for (int i=0;i<n;i++) {
            auto [lo,hi]=integer_bounds(matrices[i],v);
            if (lo>hi) {integral=0;break;}
            if (lo!=hi) unique=false;
            candidate[i]=lo;
        }
        if (integral<0 && unique) integral=dimension_character(t,n,candidate) ? 1 : 0;
    }
    if (integral == 1) return {1,1};
    if (weak < 0) {
        auto [lo,hi]=integer_bounds(omega,v);
        if (lo>hi) weak=0;
        else if (lo==hi) weak=psd_singular(omega,lo) ? 1 : 0;
    }
    return {integral,weak};
}

static unsigned properties(const std::vector<int>& t,int n) {
    auto at=[&](int i,int j,int k){return t[(i*n+j)*n+k];};
    std::vector<int> dual(n),invertibles;
    unsigned flags=0;
    bool commutative=true,selfdual=true;
    std::vector<std::vector<unsigned>> support(n,std::vector<unsigned>(n));
    std::vector<Matrix> matrices(n,Matrix(n,std::vector<long long>(n)));
    Matrix sum(n,std::vector<long long>(n)),omega(n,std::vector<long long>(n));
    for (int i=0;i<n;i++) {
        int hits=0;
        for (int j=0;j<n;j++) {
            if (at(0,i,j)!=(i==j) || at(i,0,j)!=(i==j)) throw std::runtime_error("Invalid unit");
            if (at(i,j,0)) {if(at(i,j,0)!=1)throw std::runtime_error("Invalid duality");dual[i]=j;hits++;}
            for (int k=0;k<n;k++) {
                int v=at(i,j,k);
                if (v) support[i][j] |= 1u<<k;
                matrices[i][j][k]=v;sum[j][k]+=v;
                if (v!=at(j,i,k))commutative=false;
            }
        }
        if(hits!=1)throw std::runtime_error("Invalid duality count");
        if(dual[i]!=i)selfdual=false;
        if(support[i][dual[i]]==1u)invertibles.push_back(i);
    }
    for(int i=0;i<n;i++)for(int j=0;j<n;j++)for(int k=0;k<n;k++) {
        if(dual[dual[i]]!=i || at(i,j,k)!=at(dual[i],k,j))
            throw std::runtime_error("Invalid Frobenius reciprocity");
    }
    bool simple=true;
    for(int generator=1;generator<n && simple;generator++) {
        unsigned found=1u|(1u<<generator)|(1u<<dual[generator]);
        for(;;) {
            unsigned old=found;
            for(int i=0;i<n;i++)if(old&(1u<<i)) {
                found|=1u<<dual[i];
                for(int j=0;j<n;j++)if(old&(1u<<j))found|=support[i][j];
            }
            if(found==old)break;
        }
        if(found!=(1u<<n)-1)simple=false;
    }
    if(simple)flags|=1u<<2;
    if(invertibles.size()==1)flags|=1u<<3;
    if(int(invertibles.size())==n)flags|=1u<<4;
    if(commutative)flags|=1u<<5;
    if(selfdual)flags|=1u<<6;
    if(*std::max_element(t.begin(),t.end())==1)flags|=1u<<7;

    // Frobenius reciprocity gives N_i^T=N_{i*}, so omega is symmetric,
    // nonnegative, with Perron eigenvalue sum_i FPdim(X_i)^2.
    for(int j=0;j<n;j++)for(int k=j;k<n;k++) {
        long long value=0;
        for(int i=0;i<n;i++)for(int l=0;l<n;l++)value+=matrices[i][j][l]*matrices[i][k][l];
        omega[j][k]=omega[k][j]=value;
    }
    std::vector<long double> approx(n,1);
    for(int step=0;step<80;step++) {
        std::vector<long double> next(n);
        for(int i=0;i<n;i++)for(int j=0;j<n;j++)next[i]+=sum[i][j]*approx[j];
        long double normal=next[0];
        for(int i=0;i<n;i++)next[i]/=normal;
        approx=next;
    }
    std::vector<I> rational(n);
    for(int i=0;i<n;i++) {
        long double value=std::round(approx[i]*1000000000000.0L);
        if(!std::isfinite(value) || value<1 || value>1e25L)throw std::runtime_error("Rational proposal out of range");
        rational[i]=I(value);
    }
    auto [integral,weak]=dimension_flags(t,n,matrices,omega,rational);
    if(integral<0 || weak<0) {
        std::vector<cpp_int> v(n,1);
        for(int step=0;step<160 && (integral<0 || weak<0);step++) {
            std::vector<cpp_int> next(n);
            for(int i=0;i<n;i++)for(int j=0;j<n;j++)next[i]+=sum[i][j]*v[j];
            v=next;
            if(step%8==7) {
                auto result=dimension_flags(t,n,matrices,omega,v,integral,weak);
                integral=result.first;weak=result.second;
            }
        }
    }
    if(integral<0 || weak<0)throw std::runtime_error("Exact FP-dimension bounds undecided");
    if(integral)flags|=1u;
    if(weak)flags|=2u;
    return flags;
}

int main(int argc,char** argv) {
    try {
        if(argc!=4)throw std::runtime_error("Usage: census_properties RANK FLAGS_FILE TENSORS_FILE");
        int n=std::stoi(argv[1]);if(n<2||n>12)throw std::runtime_error("Rank out of range");
        std::ofstream flags(argv[2],std::ios::binary),tensors(argv[3],std::ios::binary);
        if(!flags||!tensors)throw std::runtime_error("Cannot open output files");
        std::string line;size_t count=0;
        while(std::getline(std::cin,line)) {
            std::vector<int> t;int value=-1;
            for(char c:line) {
                if(c>='0'&&c<='9')value=(value<0?0:value)*10+(c-'0');
                else {if(value>=0){t.push_back(value);value=-1;}if(c!='{'&&c!='}'&&c!='['&&c!=']'&&c!=','&&c!=' '&&c!='\r'&&c!='\t')throw std::runtime_error("Unexpected tensor syntax");}
            }
            if(value>=0)t.push_back(value);
            if(t.size()!=size_t(n*n*n))throw std::runtime_error("Invalid tensor length");
            unsigned m=*std::max_element(t.begin(),t.end());
            if(m<1||m>65535)throw std::runtime_error("Coefficient out of uint16 range");
            u16(flags,m);u16(flags,properties(t,n));
            for(int x:t)u16(tensors,unsigned(x));
            count++;
        }
        if(!flags||!tensors)throw std::runtime_error("Output write failed");
        std::cerr<<"Exact structural flags and tensor bytes: rank "<<n<<", "<<count<<" rings\n";
    } catch(const std::exception& e) {std::cerr<<e.what()<<"\n";return 1;}
}

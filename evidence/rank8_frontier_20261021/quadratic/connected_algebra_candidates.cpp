// Exact finite necessary underlying-object test for connected separable algebras.
// Uses no floating point, search cutoff, or assertion-only checks.
#include <array>
#include <iostream>
#include <stdexcept>
#include <vector>
// Entry bounds <=400 make signed __int128 exact: every stored order-r
// minor, r<=6, has absolute value <=6^3*400^6 by Hadamard. An update
// numerator is at most twice the square of this, <2^127. The final
// order-seven minor is formed in the last such safe update.
using Exact=__int128;
using Vec=std::array<int,8>;
int R[8][8][8],upper[8],dual[8],id;
Vec a;
std::vector<int> representatives;
unsigned long long tested=0, entry_pass=0, psd_pass=0, stabilizer_pass=0;
bool first=true;

bool psd(const int V[8][8]) {
    Exact M[7][7];
    for(int i=0;i<7;++i) for(int j=0;j<7;++j) M[i][j]=V[i+1][j+1];
    Exact previous=1;
    for(int k=0;k<7;++k) {
        int pivot=-1;
        for(int i=k;i<7;++i) {
            if(M[i][i]<0) return false;
            if(M[i][i]>0 && pivot<0) pivot=i;
        }
        if(pivot<0) {
            for(int i=k;i<7;++i) for(int j=k;j<7;++j) if(M[i][j]!=0) return false;
            return true;
        }
        if(pivot!=k) {
            for(int j=0;j<7;++j) std::swap(M[k][j],M[pivot][j]);
            for(int i=0;i<7;++i) std::swap(M[i][k],M[i][pivot]);
        }
        Exact p=M[k][k];
        for(int i=k+1;i<7;++i) for(int j=i;j<7;++j) {
            Exact v=p*M[i][j]-M[i][k]*M[k][j];
            if(v%previous!=0) throw std::runtime_error("nonexact fraction-free division");
            M[i][j]=v/previous; M[j][i]=M[i][j];
        }
        previous=p;
    }
    return true;
}

void check() {
    ++tested;
    // If an invertible g occurs in A then g*A is isomorphic to A as a
    // simple right A-module, hence its underlying object is g-invariant.
    for(int g=1;g<8;++g) if(upper[g]==1 && a[g]==1) {
        bool invertible=true;
        for(int k=0;k<8;++k) if(R[g][dual[g]][k]!=(k==0)) invertible=false;
        if(!invertible) continue;
        for(int k=0;k<8;++k) {
            int coeff=0;for(int i=0;i<8;++i)coeff+=a[i]*R[g][i][k];
            if(coeff!=a[k]) return;
        }
    }
    ++stabilizer_pass;
    int V[8][8];
    for(int i=0;i<8;++i) for(int j=i;j<8;++j) {
        int v=-a[i]*a[j];for(int k=0;k<8;++k)v+=a[k]*R[k][i][j];
        if(v<0)return;
        if(v>400)throw std::runtime_error("entry exceeds proved exact arithmetic bound");
        V[i][j]=V[j][i]=v;
    }
    ++entry_pass;
    for(int j=0;j<8;++j) if(V[0][j]!=0) throw std::runtime_error("unit row not zero");
    if(!psd(V))return;
    ++psd_pass;
    if(!first)std::cout<<','; first=false;
    std::cout<<'[';for(int i=0;i<8;++i){if(i)std::cout<<',';std::cout<<a[i];}std::cout<<']';
}

void search(unsigned at) {
    if(at==representatives.size()){check();return;}
    int i=representatives[at];
    for(int v=0;v<=upper[i];++v){a[i]=a[dual[i]]=v;search(at+1);}
}

int main() {
    if(!(std::cin>>id))return 1;
    for(int i=0;i<8;++i)std::cin>>upper[i];
    for(int i=0;i<8;++i)std::cin>>dual[i];
    for(int i=0;i<8;++i)for(int j=0;j<8;++j)for(int k=0;k<8;++k)std::cin>>R[i][j][k];
    if(!std::cin)throw std::runtime_error("incomplete exact input");
    a.fill(0);a[0]=1;
    for(int i=1;i<8;++i)if(i<=dual[i])representatives.push_back(i);
    std::cout<<"{\"id\":"<<id<<",\"necessary_survivor_vectors\":[";
    search(0);
    std::cout<<"],\"bounded_selfdual_vectors_tested\":"<<tested
      <<",\"invertible_stabilizer_survivors\":"<<stabilizer_pass
      <<",\"entrywise_Gram_survivors\":"<<entry_pass
      <<",\"PSD_Gram_survivors\":"<<psd_pass<<"}\n";
}

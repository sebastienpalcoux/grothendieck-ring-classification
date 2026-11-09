// Exact row reduction and exhaustive bounded integer solutions.
// Certified input ranges: 0 <= M <= 59, coefficient magnitudes <= 59,
// and right-hand-side magnitudes <= 10443. Intermediate minors and
// Bareiss products fit signed 128-bit integers; see census/README.md.
#pragma once
#include <algorithm>
#include <stdexcept>
namespace census {
using Integer = long long;
using Wide = __int128_t;
template<class Callback>
void integer_box(Wide A[5][6], Integer M, Callback&& callback) {
 using I = Integer;
 using W = Wide;
 if (M < 0 || M > 59) throw std::invalid_argument("integer-box bound");

  int piv[5],freevars[5],rank=0,nfree=0;W previous=1;
  for(int col=0;col<5;++col){
   int pr=rank;while(pr<5&&A[pr][col]==0)++pr;
   if(pr==5){freevars[nfree++]=col;continue;}
   if(pr!=rank)for(int k=0;k<6;++k)std::swap(A[pr][k],A[rank][k]);
   W pivot=A[rank][col];
   for(int row=rank+1;row<5;++row){
    W q=A[row][col];
    for(int k=col+1;k<6;++k){
     W num=pivot*A[row][k]-q*A[rank][k];
     if(previous!=1){if(num%previous)throw std::logic_error("nonexact fraction-free division");num/=previous;}
     A[row][k]=num;
    }
    A[row][col]=0;
   }
   piv[rank++]=col;previous=pivot;
  }
  for(int row=rank;row<5;++row)if(A[row][5])return;
  // Necessary bounds on each exact linear equation over the integer box.
  for(int row=0;row<rank;++row){
   W lo=0,hi=0;for(int k=0;k<5;++k){W v=A[row][k]*M;if(v<0)lo+=v;else hi+=v;}
   if(A[row][5]<lo||A[row][5]>hi)return;
  }
  I x[5]{};
  auto enumerate=[&](auto&& self,int depth)->void{

   if(depth<nfree){
    int col=freevars[depth];W low=0,high=M;
    auto floordiv=[](W a,W b){W q=a/b;if(a%b<0)--q;return q;};
    auto ceildiv=[](W a,W b){W q=a/b;if(a%b>0)++q;return q;};
    for(int row=0;row<rank;++row){
     W rhs=A[row][5],lo=0,hi=0;
     for(int k=0;k<5;++k){
      if(k==col)continue;
      bool assigned=false;for(int z=0;z<depth;++z)if(freevars[z]==k)assigned=true;
      if(assigned)rhs-=A[row][k]*x[k];
      else{W v=A[row][k]*M;if(v<0)lo+=v;else hi+=v;}
     }
     W q=A[row][col];
     if(q==0){if(rhs<lo||rhs>hi)return;continue;}
     W l=rhs-hi,h=rhs-lo;if(q<0){W temp=l;l=-h;h=-temp;q=-q;}
     low=std::max(low,ceildiv(l,q));high=std::min(high,floordiv(h,q));
     if(low>high)return;
    }
    for(I v=static_cast<I>(low);v<=static_cast<I>(high);++v){x[col]=v;self(self,depth+1);}return;
   }

   for(int row=rank-1;row>=0;--row){
    int col=piv[row];W rhs=A[row][5];for(int k=col+1;k<5;++k)rhs-=A[row][k]*x[k];
    W pv=A[row][col];if(rhs%pv)return;W val=rhs/pv;if(val<0||val>M)return;x[col]=static_cast<I>(val);
   }
   callback(x);
  };
  enumerate(enumerate,0);

}
}  // namespace census

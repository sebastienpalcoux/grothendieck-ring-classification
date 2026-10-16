// Complete rank-four census. Integer elimination, no imported list.
// See finite_sections/census.tex for all branches and the completeness proof.
#include <array>
#include <cmath>
#include <iostream>
#include <stdexcept>
using I=long long;
using P=std::array<I,10>;
bool valid(const P&p){auto[a,b,c,d,e,f,g,h,i,j]=p;return
 a*d-b*b+b*g+c*h-d*d-e*e+1==0&&a*e-b*c+b*h+c*i-d*e-e*f==0&&
 b*e-c*d+d*h-e*g+e*i-f*h==0&&a*f+b*i-c*c+c*j-e*e-f*f+1==0&&
 b*f-c*e+d*i-e*h+e*j-f*i==0&&d*f-e*e+g*i-h*h+h*j-i*i+1==0;}
int main(int argc,char**argv){
 if(argc!=2)return 2;
 I M=std::stoll(argv[1]);
 // All intermediates are bounded by 20(M+1)^5 < 2^63 for M<=1000.
 if(M<1||M>1000)throw std::invalid_argument("bound must lie in [1,1000]");
 auto has=[&](I x){return 0<=x&&x<=M;};
 auto emit=[&](P p){if(valid(p)){std::cout<<"S";for(I v:p)std::cout<<' '<<v;std::cout<<'\n';}};
 // Swapping y,z allows b<=c; canonicalization removes remaining repetitions.
 for(I a=0;a<=M;++a)for(I b=0;b<=M;++b)for(I c=b;c<=M;++c)
 for(I d=0;d<=M;++d)for(I e=0;e<=M;++e)for(I f=0;f<=M;++f){
  if(b){
   I H=e*(d+f-a)+b*c, G=b*b+d*d+e*e-a*d-1;
   I J=c*c+e*e+f*f-a*f-1;
   I A=e*(b*b-c*c)+b*c*(f-d);
   I B=b*b*b*e-b*b*c*d+b*(d-f)*H-e*b*G+e*c*H;
   auto finish=[&](I i){
    I hh=H-c*i;if(hh%b)return;I h=hh/b;if(!has(h))return;
    I gg=G-c*h;if(gg%b)return;I g=gg/b;if(!has(g))return;
    I jj=J-b*i;if(jj%c)return;I j=jj/c;if(!has(j))return;
    emit({a,b,c,d,e,f,g,h,i,j});
   };
   if(A){if(B%A==0&&has(-B/A))finish(-B/A);}
   else if(B==0)for(I i=0;i<=M;++i)finish(i);
  }else if(c){
   I hh=d*d+e*e-a*d-1,ii=e*(d+f-a),jj=c*c+e*e+f*f-a*f-1;
   if(hh%c||ii%c||jj%c)continue;
   I h=hh/c,i=ii/c,j=jj/c;if(!has(h)||!has(i)||!has(j))continue;
   I gg=h*(d-f)+e*i-c*d;
   if(e){if(gg%e==0&&has(gg/e))emit({a,b,c,d,e,f,gg/e,h,i,j});}
   else if(gg==0)for(I g=0;g<=M;++g)emit({a,b,c,d,e,f,g,h,i,j});
  }else{
   if(a*d-d*d-e*e+1||e*(a-d-f)||a*f-e*e-f*f+1)continue;
   for(I h=0;h<=M;++h)for(I i=0;i<=M;++i){
    I gg=h*(d-f)+e*i,jj=e*h+i*(f-d);
    if(e){if(gg%e==0&&jj%e==0&&has(gg/e)&&has(jj/e))emit({a,b,c,d,e,f,gg/e,h,i,jj/e});}
    else if(gg==0&&jj==0)for(I g=0;g<=M;++g)for(I j=0;j<=M;++j)emit({a,b,c,d,e,f,g,h,i,j});
   }
  }
 }
 // The fourth non-self-dual equation fixes the nonnegative integer f.
 for(I c=0;c<=M;++c)for(I d=0;d<=M;++d)for(I e=0;e<=M;++e){
  I q=1+c*c-d*d+e*e;if(q<0)continue;
  I f=static_cast<I>(std::sqrt(static_cast<double>(q)));
  while((f+1)*(f+1)<=q)++f;while(f*f>q)--f;
  if(f*f!=q||!has(f))continue;
  auto finish=[&](I b){
   I rhs=b*b-2*b*e+c*c+d*d-1;
   auto test=[&](I a){if(a*c-b*b+2*b*e-c*c-d*d+1==0&&
    a*d-b*b+b*e+b*f-2*c*d==0&&b*(c-d)+d*(e-f)==0)
     std::cout<<"N "<<a<<' '<<b<<' '<<c<<' '<<d<<' '<<e<<' '<<f<<'\n';};
   if(c){if(rhs%c==0&&has(rhs/c))test(rhs/c);}
   else if(d){rhs=b*b-b*e-b*f+2*c*d;if(rhs%d==0&&has(rhs/d))test(rhs/d);}
   else for(I a=0;a<=M;++a)test(a);
  };
  if(c!=d){I rhs=-d*(e-f);if(rhs%(c-d)==0&&has(rhs/(c-d)))finish(rhs/(c-d));}
  else if(d*(e-f)==0)for(I b=0;b<=M;++b)finish(b);
 }
}

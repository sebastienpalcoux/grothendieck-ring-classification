"""Exact cyclic quartic sphericality certificate for the rank-five manuscript.

Standard Python 3.10+. All arithmetic controlling the census is integer
or rational; radical cutoffs are rounded outward with integer square roots.
"""

if not __debug__:
    raise RuntimeError("Run this verifier with Python assertions enabled")

from fractions import Fraction as Q
from math import isqrt,gcd,lcm
from functools import cache
from math import prod
from itertools import product
from collections import Counter
def local_packets(mod):
 fs=[];n=mod;p=2
 while p*p<=n:
  if n%p==0:
   a=0
   while n%p==0:n//=p;a+=1
   fs.append((p,a))
  p+=1
 if n>1:fs.append((n,1))
 parts=[]
 for p,e in fs:
  if p==2:
   if e==2: loc=[(2,1)]
   elif e==3:loc=[(0,1),(2,1)]
   elif e==4:loc=[(x,8) for x in (0,2) for _ in (1,3)]
   else:return []
  elif e==1:loc=[((t*((p-1)//2))%4,p if t%2 else 1) for t in (1,2,3) if t*(p-1)%4==0]
  else:return []
  parts.append(loc)
 return [(sum(p[0] for p in a)%4,prod(x[1] for x in a)) for a in product(*parts)]
def field_counts():
 answer=Counter()
 for j in range(15,729):
  c=Counter(f for parity,f in local_packets(j) if parity==0 and 1<f<40)
  for f,n in c.items():
   assert n%2==0
   answer[f,j]=n//2
 return answer

@cache
def divs(n):return sorted({x for i in range(1,isqrt(n)+1) if n%i==0 for x in (i,n//i)})
QUADRATIC_CONDUCTORS = field_counts()

def sqrt_upper(x, digits=10**10):
    x=Q(x)
    return Q(isqrt((x.numerator*digits**2)//x.denominator)+1,digits)

@cache
def bounds(F,J,f=0,g=4):
    # Outward rational upper bounds for all radicals in the trace cutoff.
    t=1-Q(1,g); s=1-Q(1,f) if f else Q(1)
    quad=sqrt_upper(Q(gcd(F,4),F))
    adj=sqrt_upper(Q(2*gcd(J,4),J))
    q0=sqrt_upper(sqrt_upper(Q(1,g*F*J*J)))
    v0=(t-quad)/2; v1=(t-adj)/2
    b0=max(v0/2,v0-q0); b1=max(v1/2,v1-q0)
    assert min(b0,b1)>0, "trace cutoff requires positive conjugate bounds"
    U=1+s/min(b0,b1)
    if b0<=b1:
        w2=min(s,(s+sqrt_upper(Q(2,F)))/2)
        U=min(U,1+(s-w2)/b1+w2/b0)
    return U
def fields(F): return [j for (f,j) in QUADRATIC_CONDUCTORS if f==F]
@cache
def minB(F):
 return max(bounds(F,J) for J in fields(F))
def polys(F):
 z=F if F%4 else F//4
 Am=int(minB(F))+1;As=list(range(4,Am+1))
 # H+L√z=4(α0−α2)^2 and H−L√z=4(α1−α3)^2; hence H<=2A² by convexity over coset sums.
 ww={}
 for h in range(1,2*Am*Am//z+1):
  R=z*h*h
  w0=[L for L in range(isqrt(R)+1) if (w:=isqrt(R-L*L))>0 and w*w==R-L*L]
  if w0:ww[h]=w0
 for A in As:
  for B in range(0,A//isqrt(z)+1):
   if B*B*z>=A*A or (z*B-A)%2:continue
   for h in range(1,(A*A+z*B*B)//z+1):
    if h not in ww:continue
    H=z*h
    if (A*A+z*B*B-H)%8:continue
    C=(A*A+z*B*B-H)//8
    if C<=0:continue
    for v in ww[h]:
     for L in ({v,-v} if B and v else {v}):
      if (2*A*B-L)%8:continue
      D=(2*A*B-L)//8
      if (z*D-C)%2 or z*D*D>=C*C:continue
      c2n=(A*A-z*B*B)+4*C
      c3n=A*C-z*B*D
      c4n=C*C-z*D*D
      if c2n%4 or c3n%2 or c4n%4:continue
      c2=c2n//4;c3=c3n//2;c4=c4n//4
      if 27*c4>=A**3:continue # min conjugate <1
      if A**4%c4 or c2**4%c4**2 or c3**4%c4**3:continue
      # All four roots are positive by the pair sums and products.
      # Exclude all roots >= 1 using the elementary symmetric functions
      # of the four real roots after subtracting one.
      shifted=(A-4,c2-3*A+6,c3-2*c2+3*A-4,c4-c3+c2-A+1)
      if min(shifted)>=0:continue
      yield A,B,h,L,C,D,c2,c3,c4
def census():
 tally=Counter();res=[]
 for F in sorted({F for F,J in QUADRATIC_CONDUCTORS}):
  js=fields(F);z=F if F%4 else F//4
  for t in polys(F):
   A,B,h,L,C,D,u,v,w=t
   # pairs; actual J must divide discriminant of defining polynomial on the primitive order
   # resultant of two quadratics g,gbar: Norm(difference) elementary; evaluate using direct discr formula via e_i
   # discr=[(α0−α2)(α1−α3)]² Res(g,gbar)^2
   # g-gbar=√z(D-BX) ; Res(g,gbar)=z [D²-B D(A+B√z)/2+B²(C+D√z)/2] =z(2D²−ABD+B²C)/2.
   RR=abs(z*(2*D*D-A*B*D+B*B*C))
   WW=isqrt(z*h*h-L*L)
   if not RR:continue
   # sqrt(discr/F)=RR*WW/8 if F=z; /16 if F=4z
   Jmult=RR*WW//(8 if F==z else 16)
   if Jmult*(8 if F==z else 16)!=RR*WW:raise ValueError
   possible=[j for j in js if Jmult%j==0 and A<=bounds(F,j)]
   if not possible:continue
   tally['alpha']+=1
   for r in range(1,A//4+1):
    if isqrt(r*w)**2!=r*w:continue
    gg=gcd(gcd(A-4*r,u-6*r*r),gcd(v-4*r**3,w-r**4))
    if not gg:continue
    for g in divs(abs(gg)):
     if g%r or g//r<4:continue
     f=g//r
     Jlist=tuple(j for j in possible if A<=bounds(F,j,f,g))
     if not Jlist:continue
     res.append((F,A,B,h,L,C,D,u,v,w,r,f,g,Jlist))
 print('Distinct field-polynomial profiles before the rational-axis test:',tally['alpha'])
 return res

def kmul(x,y,z):
 return (x[0]*y[0]+z*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def neg(a):return tuple(-x for x in a)
def kc(a):return a[0],-a[1]
def kn(a,z):return a[0]**2-z*a[1]**2
def mul(u,v,z,H,L):
 a,b=u[:2],u[2:]; c,d=v[:2],v[2:]
 return add(kmul(a,c,z),kmul((H,L),kmul(b,d,z),z))+add(kmul(a,d,z),kmul(b,c,z))
def norm(u,z,H,L):
 a,b=u[:2],u[2:]
 return kn(add(kmul(a,a,z),neg(kmul((H,L),kmul(b,b,z),z))),z)
def inverse_matrix(M):
 N=len(M);m=[[Q(a) for a in v]+[Q(i==j) for j in range(N)] for i,v in enumerate(M)]
 for i in range(N):
  j=next(j for j in range(i,N) if m[j][i])
  m[i],m[j]=m[j],m[i]
  m[i]=[a/m[i][i] for a in m[i]]
  for j in range(N):
   if i!=j:m[j]=[a-m[j][i]*b for a,b in zip(m[j],m[i])]
 return [v[N:] for v in m]
def matvec(M,b):return tuple(sum(vj*bj for vj,bj in zip(v,b)) for v in M)
def rows(qq):
 F,A,B,h,L,C,D,u,v,w,r,f,g,Js=qq
 z=F if F%4 else F//4
 H=z*h;W=isqrt(z*h*h-L*L)
 one=(1,0,0,0);al=(Q(A,4),Q(B,4),Q(1,4),0)
 # sigma(Wrad)=W*sqrt(z)/Wrad=(H/(z W)*sqrt(z)-L/W)*Wrad.
 al1=(Q(A,4),Q(-B,4),Q(-L,4*W),Q(H,4*z*W))
 al2=(Q(A,4),Q(B,4),Q(-1,4),0)
 a2=mul(al,al,z,H,L)
 fs=[one,al,al1,al2 if B else a2]
 basis=[tuple(int(i==j) for i in range(4)) for j in range(4)]
 inv=inverse_matrix([[4*mul(elt,ee,z,H,L)[0] for ee in basis] for elt in fs])
 s=1-Q(1,f);t=1-Q(1,g);N=int(A*t-4*s)
 assert N==A*t-4*s
 for n1 in range(N+1):
  for n2 in (range(N-n1+1) if B else range(1,A+3)):
   if not B and n1+Q(A,2)*t-2*s>N:continue
   y=matvec(inv,[t,s,s+n1,s+n2 if B else n2-Q(r*r,g)])
   no=norm(y,z,H,L)
   if no<=0 or no.numerator!=1:continue
   NE=no.denominator
   ND0=NE//w
   if NE%w or NE<g*F*min(Js)**2 or ND0<f*F*min(Js)**2: continue
   if isqrt(g*NE*F)**2!=g*NE*F:continue
   yield y,NE,ND0

def fourier_squares(y,z,H,L):
    a,b,v,w=y
    return (16*z*b*b,8*(H*(v*v+z*w*w)+2*z*L*v*w))

def main():
    print("Real cyclic quartic fields:",sum(QUADRATIC_CONDUCTORS.values()))
    profiles=census()
    norm_candidates=0
    matches=0
    for x in profiles:
        F,A,B,h,L,*other=x
        J=min(x[-1])
        z=F if F%4 else F//4
        H=z*h
        al=(Q(A,4),Q(B,4),Q(1,4),0)
        for y,NE,ND in rows(x):
            norm_candidates+=1
            p=mul(al,y,z,H,L)
            p2,p4=fourier_squares(p,z,H,L)
            q2,q4=fourier_squares(y,z,H,L)
            if 2*p2+q2<=Q(4,F) and 2*p4+q4<=Q(4,J):
                matches+=1
    counts=(len(profiles),norm_candidates,matches)
    print("alpha/f/g profiles, trace and norm candidates, Fourier-compatible:",counts)
    assert counts==(32,10,0)
if __name__=="__main__": main()

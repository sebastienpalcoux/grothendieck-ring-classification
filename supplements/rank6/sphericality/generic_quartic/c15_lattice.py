"""Test the residual ratio X^4-7X^3+14X^2-8X+1 in its coefficient-dual lattice."""
from itertools import product
from fractions import Fraction as F
from math import gcd,lcm,prod,isqrt
import sympy as sp
X=sp.symbols('X')
P=sp.Poly(X**4-7*X**3+14*X**2-8*X+1,X)
def reduce(a):return sp.rem(a,P.as_expr(),X).expand()
def coords(a):return [int(a.expand().coeff(X,i)) for i in range(4)]
def multiplication(a):return sp.Matrix([coords(reduce(a*X**i)) for i in range(4)]).T
trace=[int(multiplication(X**i).trace()) for i in range(4)]
def tr(a):return sum(i*j for i,j in zip(coords(reduce(a)),trace))
tau=4*X-X*X
others=[1+8*X-6*X**2+X**3,6-13*X+7*X**2-X**3]
for a in (tau,*others):
 print('automorphism',a,'square',reduce(a.subs(X,a)))
tau=[a for a in (tau,*others) if reduce(a.subs(X,a))==X][0]
basis=[1,X-2,(X-2)**2-2,(X-2)**3-3*(X-2)]
B=sp.Matrix([[tr((tau-X)*b*X**j) for j in range(4)] for b in basis])
L=B.inv()
den=int(sp.ilcm(*[sp.denom(c) for c in L]));lat=[[int(c*den) for c in L.row(i)] for i in range(4)]
xt=[tr(X**(j+1)) for j in range(4)]
roots=P.intervals(eps=sp.Rational(1,10**12))
real=[(F(int(l.p),int(l.q)),F(int(h.p),int(h.q))) for ((l,h),_) in roots]
assert real[0][0]>0 and real[-1][1]<4
def eval_interval(coeff,ab):
    lo=hi=F(0)
    for v in reversed(coeff):
        k=[u*w for u in (lo,hi) for w in ab]
        lo,hi=min(k)+v,max(k)+v
    return lo,hi
multis=[multiplication(X**i) for i in range(4)]
found=0;cnt={}
for ns in product(range(-3,4),range(-7,8),range(-7,8),range(-7,8)):
    cc=[sum(u*v for u,v in zip(row,ns)) for row in lat]
    tt=sum(u*v for u,v in zip(cc,trace));ss=sum(u*v for u,v in zip(cc,xt))
    if tt*25<16*den or tt>=den or not 0<ss<den:continue
    # exact positivity & minimum handled below after the necessary norm condition
    q=sum((int(w)*m for w,m in zip(cc,multis)),sp.zeros(4))
    n=int(q.det())
    if n<=0 or den**4%n:continue
    E=den*q.inv()
    pchar=E.charpoly().all_coeffs()
    if any(not u.is_integer for u in pchar):continue
    pc=[int(i) for i in pchar]
    if any(pc[i]**4%pc[-1]**i for i in (1,2,3)):continue
    q_intervals=[eval_interval(cc,z) for z in real]
    p_intervals=[eval_interval([0]+cc,z) for z in real]
    if any(hi<=0 for lo,hi in q_intervals): continue
    if any(rr[0][0]>hi for rr in (q_intervals,p_intervals) for lo,hi in rr):continue
    found+=1
assert found==0
print('The signed codifferent excludes the conductor-15 residual ratio.')

"""Outward interval certificate for the four small moments at conductor 24. Run with Python 3."""
import sys,itertools,math
from math import isqrt
S = 10**9
class I:
    def __init__(self, lo, hi=None):
        self.lo, self.hi = lo, (lo if hi is None else hi)
    def __add__(self, y): return I(self.lo+y.lo, self.hi+y.hi)
    def __sub__(self, y): return I(self.lo-y.hi, self.hi-y.lo)
    def __mul__(self, y):
        v = [a*b for a in (self.lo,self.hi) for b in (y.lo,y.hi)]
        return I(min(v)//S,-(-max(v)//S))
    def __truediv__(self, y):
        assert y.lo>0
        return self*I(S*S//y.hi,-(-S*S//y.lo))
    def cap(self, y):
        return I(max(self.lo,y.lo), min(self.hi,y.hi))
    def empty(self): return self.lo>self.hi
    def sq(self):
        v=self*self
        return I(max(0,v.lo),v.hi)
def n(x): return I(x*S)
def rt(x):
    a=isqrt(x*S*S)
    return I(a,a+1)
zero=n(0); one=n(1); two=n(2)
unit=I(0,S); eps=I(0,S//500000)

from fractions import Fraction as F

e=I(0,S//250000)
def absI(x):return I(max(0,x.lo,-x.hi), max(x.hi,-x.lo))
def mark(iv,name):
 b=extrema.setdefault(name,[10**20,-10**20])
 b[0]=min(b[0],iv.lo);b[1]=max(b[1],iv.hi)
def process(z,y,w,arg,cond,depth):
 # <=e for q0,qj,p0; p_j=z, q_l=(1-q0-qj+y)/2, p_l=(1−p0-z+w)/2, y≥0.
 # w is signed p_l-p_m. Given H or K fixed solve a,r.
 d,c,f=cond; qsmall=two*e
 qm=(one-qsmall-y)/two;ql=qm+y
 pm=(one-e-z-w)/two;pl=pm+w
 if qm.hi<S//12 or pm.hi<S//50 or pl.hi<S//50:return
 qm=qm.cap(I(S//12,S));ql=ql.cap(I(S//2-2*e.hi,S))
 pl=pl.cap(I(S//50,S));pm=pm.cap(I(S//50,S))
 P=z+e
 for c0,pv,qv in [(d,two*P-one,one-two*qsmall),(c,e-z+w,y+I(-e.hi,e.hi)),(f,e-z-w,y+I(-e.hi,e.hi))]:
  if (n(c0)*pv.sq()+two*rt(c0)*absI(qv)).lo>8*S:return
  if (n(c0)*qv.sq()).lo>16*S:return
 A=pl/ql; B=pm/qm
 h,k=arg
 r=((n(h)-ql*B-qm*A-e)/z).cap(unit) # H=zr+qj a+qlB+qm A
 if r.empty():return
 a=((n(k)-(one-qsmall)*A*B)/(z*(one+r))).cap(I(0,min(S,A.hi,B.hi)))
 if a.empty():return
 if r.lo>0:
  s=qm/ql
  Sr=r+one/r
  Ss=s+one/s
  # Norm obstruction OR quadratic W; if sep from zero and norm <1 then impossible.
  diff=Sr-Ss
  if (diff.lo>0 or diff.hi<0) and ((one+r)*e*diff.sq()).hi<S:return
 # Compare squared norms of the ordinary and signed simultaneous induction columns.
 p=[e,z,pl,pm];q=[e,e,ql,qm]
 for i in (1,2,3):
  j=i
  # p0 sum_lt_ne0 p_{i+l} p_{j+l}/p_l <=e(1/z+1/pl+1/pm)
  corr=e*(one/z+one/pl+one/pm)
  if (p[i]*p[j]+corr-a*(q[i]*q[j]+r*q[i^1]*q[j^1])).hi<0:return
 if depth:
  ivs=[z,y,w];lens=[iv.hi-iv.lo for iv in ivs];i=max(range(3),key=lens.__getitem__)
  lo=ivs[i].lo;hi=ivs[i].hi;m=(lo+hi)//2
  for lower,upper in ((lo,m),(m,hi)):
   v=ivs[:];v[i]=I(lower,upper);process(*v,arg,cond,depth-1)
  return
 for t,sym in [(z,'z'),(qm/ql,'s'),(r,'r'),(a,'a'),(A,'A'),(B,'B'),(y,'dyq'),(w,'dyp')]:mark(t,sym)
def hundredths(i):
 return I(i*S//100)
if __name__=='__main__':
 for cs in itertools.permutations((8,12,24)):
  if cs[0]==24:continue
  for h,k in itertools.product((1,3,5,7,9,11),(1,3,5)):
   extrema={}
   process(I(S//5,S*4//5),I(0,S*82//100),I(-S,S),(h,k),cs,24)
   if extrema:
    print(cs,h,k,extrema)
    assert (cs,h,k)==((8,12,24),3,1)
    for label,lo,hi in [('z',228,332),('s',138,185),('a',0,232)]:
     assert extrema[label][0]>=lo*S//1000 and extrema[label][1]<=hi*S//1000

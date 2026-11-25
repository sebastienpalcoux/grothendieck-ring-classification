"""Outward interval certificate for the four small moments for the opposite collapse at conductor 16. Run with Python 3."""
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
 if qm.hi<S//25 or pm.hi<S//120 or pl.hi<S//120:return
 qm=qm.cap(I(S//25,S));ql=ql.cap(I(S//2-2*e.hi,S))
 pl=pl.cap(I(S//120,S));pm=pm.cap(I(S//120,S))
 P=z+e
 if (n(8)*(two*P-one).sq()+two*rt(8)*(one-two*qsmall)).lo>8*S:return
 # faithful Fourier modulus; |Q| >= y, |P|^2 >= (p0-z)^2+w^2
 if (n(16)*((e-z).sq()+w.sq())+n(8)*y).lo>8*S:return

 A=pl/ql; B=pm/qm
 h,k=arg
 r=((n(h)-ql*B-qm*A-e)/z).cap(I(0,3*S//1000)) # H=zr+qj a+qlB+qm A
 if r.empty():return
 a=((n(k)-(one-qsmall)*A*B)/(z*(one+r))).cap(I(0,min(S,A.hi,B.hi)))
 if a.empty():return
 # linears: absolute domination W, VV' etc
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
if __name__=='__main__':
 for h,k in itertools.product(range(1,26,2),(1,3,5,7,9)):
  extrema={}
  process(I(S//5,S*4//5),I(0,S),I(-S,S),(h,k),(8,16,16),26)
  if extrema:
   print(h,k,extrema)
   assert (h,k) in ((3,1),(7,3))
   bounds=([('z',228,323),('s',138,183),('a',0,270)] if h==3 else
           [('z',228,233),('s',54,58),('a',0,409)])
   for label,lo,hi in bounds:
    assert extrema[label][0]>=lo*S//1000 and extrema[label][1]<=hi*S//1000

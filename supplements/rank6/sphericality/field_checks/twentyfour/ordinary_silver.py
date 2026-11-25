"""Check the saturated ordinary pair at conductor 24 by exact field arithmetic."""
from fractions import Fraction as F
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from quartic24_fast import inventory

ONE = (F(1),F(0),F(0),F(0))

def scale(x,a):return tuple(a*v for v in x)
def plus(x,y):return tuple(a+b for a,b in zip(x,y))
def minus(x,y):return plus(x,scale(y,-1))
def times(x,y):
    z=[F(0)]*4
    for i,a in enumerate(x):
        for j,b in enumerate(y):
            v=i&j
            z[i^j]+=a*b*((2 if v&1 else 1)*(3 if v&2 else 1))
    return tuple(z)

def conjugate(x,j):
    return tuple((-a if (j&i) in (1,2) else a) for i,a in enumerate(x))

def divide(x,y):
    z=ONE
    for j in (1,2,3):z=times(z,conjugate(y,j))
    den=times(y,z);assert not any(den[1:]) and den[0]
    return scale(times(x,z),1/den[0])

def sign_quadratic(a,b,d):
    if not b:return (a>0)-(a<0)
    if b<0:return -sign_quadratic(-a,-b,d)
    if a>=0:return 1
    q=d*b*b-a*a;return (q>0)-(q<0)

def sign(x):
    a,b,c,d=x
    u=sign_quadratic(a,b,2); v=sign_quadratic(c,d,2)
    if not u:return v
    if not v or u==v:return u
    return u*sign_quadratic(a*a+2*b*b-3*c*c-6*d*d,2*a*b-6*c*d,2)

def run():
    counts=[0]*3
    for _,_,_,A,u,v,w,B,C,N in sorted(inventory(64)):
        counts[0]+=1
        x=(F(A,4),F(u,2),F(v,2),F(w,2))
        i=next(i for i in range(4) if all(sign(minus(conjugate(x,j),conjugate(x,i)))>=0 for j in range(4)))
        x=conjugate(x,i);y=conjugate(x,2) # fixes sqrt(2)
        q=scale(divide(minus(y,ONE),minus(y,x)),F(1,2));p=times(q,x)
        if any(sign(conjugate(q,j))<=0 for j in range(4)):continue
        counts[1]+=1
        if any(sign(minus(conjugate(q,j),q))<0 or sign(minus(conjugate(p,j),p))<0 for j in range(1,4)):continue
        counts[2]+=1
    assert counts==[69,13,0]
    print('Primitive ratios, positive q, simultaneous minima:',counts)

if __name__=='__main__':run()

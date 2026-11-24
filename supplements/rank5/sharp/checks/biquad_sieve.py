"""Check biquadratic quartic profiles of formal codegree 4 or 16, with integer arithmetic."""

if not __debug__:
    raise RuntimeError("Run this verifier with Python assertions enabled")

from fractions import Fraction
from functools import lru_cache
from math import isqrt
from itertools import product

FIELDS = ((5,8,40),(5,12,60),(5,13,65),(5,17,85),(5,21,105),(8,12,24))

@lru_cache(maxsize=None)
def pell(discriminant, limit):
    # First solution T^2-d B^2=4 (B>0) gives the smallest norm-one unit >1.
    b = 1
    while True:
        y = 4 + discriminant*b*b
        a = isqrt(y)
        if a*a == y:
            break
        b += 1
    # T_n and B_n in twice the n-th power of the fundamental unit.
    t0,t=2,a
    b0,v=0,b
    seq=[]
    while t <= limit:
        seq.append((t,v))
        t0,t=t,a*t-t0
        b0,v=v,a*v-b0
    return seq

def candidates(field, f, H):
    limit = isqrt(11*H)+2
    seq = []
    for disc in field:
        positive = pell(disc,limit)
        # 1/z_i < 11/sqrt(D) < 11/sqrt(17).  Include every inverse
        # whose trace could occur, as well as the trivial unit.
        negative = [(t,-b) for t,b in positive if t <= 4]
        seq.append(negative + [(2,0)] + positive)
    scale = isqrt(field[0]*field[1]*field[2])
    assert scale*scale == field[0]*field[1]*field[2]
    checked = 0
    passed=[]
    for (a,u),(b,v),(c,w) in product(*seq):
        den=2*(4+a*b+a*c+b*c)
        cross = a*b*c-scale*u*v*w
        checked+=1
        for x,y,z in ((a,b,c),(b,a,c),(c,b,a)):
            num = 2*((y*y-2)*(z*z-2)+y*z)+(y+z)*(cross-2*x)
            if (f-1)*num % den:
                break
        else:
            passed.append(((a,u),(b,v),(c,w)))
    return checked, passed

def admissible(units, f, field):
    # Rational bounds for either sign of the quadratic coefficient.
    pairs=[]
    for t,b in units:
        if b==0:
            pairs.append((Fraction(1),Fraction(1)))
            continue
        # Rational outward enclosures for sqrt(t^2-4).
        scale=10**8
        root=isqrt((t*t-4)*scale**2)
        lo,hi=Fraction(t*scale+root,2*scale),Fraction(t*scale+root+1,2*scale)
        pairs.append((lo,hi) if b>0 else (1/hi,1/lo))
    lows,highs=zip(*pairs)
    xlow = [lows[(i+1)%3]*lows[(i+2)%3] for i in range(3)]
    xhigh = [highs[(i+1)%3]*highs[(i+2)%3] for i in range(3)]
    plow,phigh = 1+sum(xlow),1+sum(xhigh)
    s = Fraction(f-1,f)
    if phigh <= 17*s:
        return False
    for i,c in enumerate(field):
        # Fourier coefficient: 2s(1+x_h)/P -s.
        low = 2*s*(1+xlow[i])/phigh-s
        high = 2*s*(1+xhigh[i])/plow-s
        if (low>0 and c*low*low>1) or (high<0 and c*high*high>1):
            return False
    return True


def verify():
    from verify_quartic_moments import DATA, certificate_bound
    for row in DATA:
        if '-' not in row['F']:
            continue
        field = tuple(map(int,row['F'].split('-')))
        maximum = certificate_bound(row)
        checked, integral = candidates(field,4,maximum)
        survivors = [units for units in integral if admissible(units,4,field)]
        print(field, "examined",checked,"integral second moments",len(integral),
              "remaining",survivors,flush=True)
        assert not survivors


if __name__ == "__main__":
    verify()

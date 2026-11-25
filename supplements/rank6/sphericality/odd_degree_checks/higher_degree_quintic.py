"""Check the degree-five exclusions at conductors eleven and twenty-five.

The integer interval screens include explicit bounds for int64 operations."""
from fractions import Fraction as Q
from functools import reduce
from itertools import product
from math import gcd, isqrt
from pathlib import Path
import json
import numpy as np
import sympy as sp


def is_square(n):
    return n >= 0 and isqrt(n)**2 == n


def conductor_bounds():
    # If min q >= m and min(q_0+q_i) >= a, then
    # product(q_i) >= min(m(a-m)^4,(a/2)^5), for 0<m<=a/2.
    # These rational constants apply respectively to c>=31,g>=4 and c=25,g>=6.
    for c, g, m, a in ((31,4,Q(1,220),Q(2,15)),
                       (25,6,Q(1,150),Q(23,150))):
        assert 0 < m <= a/2
        assert g*c**4*m*(a-m)**4 > 1
        assert g*c**4*(a/2)**5 > 1
    assert Q(11,2)**2 < 31                 # sqrt(31)>11/2
    assert Q(5,12)**2 > Q(5,31)            # sqrt(5/31)<5/12
    assert Q(9,20)**2 > Q(1,5)             # sqrt(1/5)<9/20
    assert Q(27,40)**2 > Q(5,11)           # sqrt(5/11)<27/40


SCALE = 10**6
INTERVALS = ((1682507,1682508),(830830,830831),(-284630,-284629),
             (-1309722,-1309721),(-1918986,-1918985))
GROUP = (1,2,4,3,5)


def index11(j):
    return min(j % 11, -j % 11)-1


def scaled_polynomial11(z):
    value = 1
    for degree, coefficient in enumerate((1,-4,-3,3,1),1):
        value = value*z + coefficient*SCALE**degree
    return value


def multiply11(c, v):
    # Coordinates in -b_j, b_j=zeta_11^j+zeta_11^-j; b_0=2=-2 sum b_j.
    out = [0]*5
    for i,x in enumerate(c,1):
        for j,y in enumerate(v,1):
            for residue in (i+j,i-j):
                k=index11(residue)
                if k<0:
                    out=[w+2*x*y for w in out]
                else:
                    out[k]-=x*y
    return out


def polynomial11(c):
    M=sp.Matrix.hstack(*[sp.Matrix(multiply11(c,[int(i==j) for i in range(5)]))
                        for j in range(5)])
    return tuple(int(z) for z in M.charpoly().all_coeffs())


def dnumber(P):
    norm=abs(P[-1])
    return norm>0 and all(abs(P[j])**5 % norm**j == 0 for j in range(1,5))


def conductor_eleven():
    assert all(scaled_polynomial11(lo)*scaled_polynomial11(hi)<0
               for lo,hi in INTERVALS)
    assert all(INTERVALS[i+1][1]<INTERVALS[i][0] for i in range(4))
    # Five disjoint sign-changing intervals account for all five roots.
    # All entries in the interval dot products are bounded by
    # 5*18*2,000,000 < 2^63, so the integer NumPy screens cannot overflow.
    assert 5*18*2000000 < 2**63
    small=np.array(list(product(range(1,19),repeat=4)),dtype=np.int64)
    lower=np.array([[INTERVALS[index11(j*h)][0] for j in range(1,6)]
                    for h in GROUP],dtype=np.int64)
    upper=lower+1
    raw=dn=0
    profiles=[]
    for first in range(1,19):
        cs=np.column_stack((np.full(len(small),first,dtype=np.int64),small))
        A=cs.sum(axis=1)
        keep=(A>5)&(A<=50)&np.all(11*cs<4*A[:,None],axis=1)
        cs=cs[keep]
        lo=-cs@upper.T
        hi=-cs@lower.T
        keep=np.all(hi>0,axis=1)&(lo[:,0]<SCALE)&np.all(lo[:,0,None]<hi,axis=1)
        for row in cs[keep]:
            c=tuple(map(int,row))
            if len(set(c))==1:
                continue
            raw+=1
            A=sum(c)
            P=polynomial11(c)
            norm=-P[-1]
            if norm<=0 or not dnumber(P):
                continue
            dn+=1
            # A ≡ 5r (mod g), g>=3r and A>0 imply r<=A.
            for r in range(1,A+1):
                if not is_square(r*norm):
                    continue
                differences=[P[j]-(-1)**j*int(sp.binomial(5,j))*r**j
                             for j in range(1,6)]
                common=reduce(gcd,map(abs,differences))
                assert common>0
                for g0 in sp.divisors(common):
                    g=int(g0)
                    if g<4 or g%r or g//r<3:
                        continue
                    f=g//r
                    t=Q(g-1,g)
                    s=Q(f-1,f)
                    if A>=1+5*s/(t-Q(27,40)):
                        continue
                    N=A*t-5*s
                    assert N.denominator==1
                    if N<0:
                        continue
                    profiles.append(dict(c=c,P=P,norm=norm,r=r,f=f,g=g,N=int(N)))
    assert (raw,dn,len(profiles))==(1838,78,2)
    expected=[((3,5,3,2,3),11,11),((4,4,4,4,2),4,8)]
    assert [(p['c'],p['f'],p['g']) for p in profiles]==expected
    for p in profiles:
        A=sum(p['c'])
        B=p['P'][2]
        # The necessary Fourier/shifted-trace inequality is c N^2<=16A^2-40B.
        assert 11*p['N']**2>16*A**2-40*B
    return dict(outer_ratios=raw,dnumber_ratios=dn,profiles=profiles)


def conductor_twenty_five():
    x=sp.symbols('x')
    phi=sp.Poly(sp.cyclotomic_poly(25,x),x)
    H=(1,7,18,24)
    periods=[sp.Poly(sum(x**((pow(2,j,25)*h)%25) for h in H),x).rem(phi)
             for j in range(5)]
    assert sum(periods,sp.Poly(0,x)).is_zero
    basis=[sp.Poly(1,x)]+periods[:4]
    embedding=sp.Matrix([[p.nth(i) for p in basis] for i in range(20)])
    table=[]
    for a in basis:
        row=[]
        for b in basis:
            p=(a*b).rem(phi)
            v=embedding.gauss_jordan_solve(sp.Matrix([p.nth(i) for i in range(20)]))[0]
            assert all(z.q==1 for z in v)
            row.append(v)
        table.append(row)
    mats=[sp.Matrix.hstack(*table[i]) for i in range(5)]
    G=sp.Matrix([[sp.trace(mats[i]*mats[j]) for j in range(5)] for i in range(5)])
    assert G==sp.Matrix([[5,0,0,0,0],[0,20,-5,-5,-5],[0,-5,20,-5,-5],
                         [0,-5,-5,20,-5],[0,-5,-5,-5,20]])
    assert G.det()==25**4
    assert mats[1].charpoly(x).as_expr()==x**5-10*x**3+5*x**2+10*x+1
    assert sp.Poly(mats[1].charpoly(x).as_expr(),x).is_irreducible
    # This integral lattice has the field discriminant, hence is O_K.
    # Trace=10 gives alpha=2+sum c_j eta_j. Positivity gives |c_j|<8*10/25,
    # and Tr(alpha^2)<100, leaving only 110 nonzero integer tuples.
    tested=0
    for c in product(range(-3,4),repeat=4):
        if c==(0,0,0,0):
            continue
        v=sp.Matrix((2,)+c)
        if (v.T*G*v)[0]>=100:
            continue
        tested+=1
        mat=2*mats[0]+sum((c[i]*mats[i+1] for i in range(4)),sp.zeros(5))
        P=[int(z) for z in mat.charpoly().all_coeffs()]
        # Positive roots require every elementary symmetric function positive.
        assert any((-1)**j*P[j]<=0 for j in range(1,6))
    assert tested==110
    return dict(integral_basis_discriminant=25**4,trace=10,
                tested_lattice_vectors=tested,totally_positive_nonrational=0)


if __name__=='__main__':
    conductor_bounds()
    result=dict(conductor_11=conductor_eleven(),conductor_25=conductor_twenty_five())
    Path(__file__).with_name('higher_degree_quintic_certificate.json').write_text(json.dumps(result,indent=2))
    print('Quintic descent certificate passed: conductors 11 and 25 only;')
    print('K_11: 1838 outer ratios, 78 d-numbers, 2 rational-axis profiles, both excluded;')
    print('K_25: 110 small-trace lattice vectors, none totally positive and nonrational.')

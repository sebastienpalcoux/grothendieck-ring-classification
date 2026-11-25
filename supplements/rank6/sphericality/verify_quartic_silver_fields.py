"""Rebuild the quartic ratio lists for fields containing sqrt(2) or sqrt(3)."""
from fractions import Fraction as F
from itertools import product
from math import gcd, isqrt
from pathlib import Path
import json
import sys

def squarefree(n):
    return all(n%(j*j) for j in range(2,isqrt(n)+1))


def discriminant(n):
    return n if n%4==1 else 4*n


def fields():
    result={}
    for rad in range(2,94**2):
        if not squarefree(rad):continue
        for base in (2,3):
            if rad==base:continue
            fld=tuple(sorted(discriminant(k) for k in (base,rad,base*rad//gcd(rad,base)**2)))
            if fld in [(5,8,40),(5,12,60),(8,12,24)] or fld[1]>=94**2:continue
            result[fld]=176 if fld==(8,28,56) else 94
    assert len(result)==4358 and sum(k[1]>=33 for k in result)==4349
    return result


def mass_bounds():
    for c,cap,cut in [(13,166,F(1,4)),(28,2718,F(27,100))]:
        h=gcd(c,4)
        assert (4/(cut**2-F(h,2*c))).__floor__()==cap
        for L in range(2*c,cap//2+1,c):
            for n in range(2*L,min(cap,(L/cut).__ceil__()-1)+1):
                d=L*L-4*n
                if L*L%n or d<=0 or d%c or 2*c*d>h*n*n:continue
                assert isqrt(d//c)**2!=d//c

S = 10**12
ROOTS = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
FILE = Path(__file__).with_name('quartic_silver_field_weights.json')


def survives(A, B, C, N):
    if min(B, C, N) <= 0:
        return False
    if min(B-3*A+6, C-2*B+3*A-4, N-C+B-A+1) > 0:
        return False
    return A**4 % N == B**4 % N**2 == C**4 % N**3 == 0


def candidates():
    out = {}
    for (d, e, f), cap in fields().items():
        k = isqrt(d*e*f)
        assert k*k == d*e*f
        for A in range(5,cap+1):
            U, V, W = [isqrt((A*A-1)//h) for h in (d, e, f)]
            for u, v in product(range(U+1), range(V+1)):
                for w in range(-W if u*v else 0, W+1):
                    if (u != 0)+(v != 0)+(w != 0) < 2:
                        continue
                    x, y, z = d*u*u, e*v*v, f*w*w
                    s, t = x+y+z, k*u*v*w
                    b8 = 3*A*A-s
                    c16 = A**3-A*s+2*t
                    n256 = A**4-2*A*A*s+8*A*t+s*s-4*(x*y+x*z+y*z)
                    if b8 % 8 or c16 % 16 or n256 % 256:
                        continue
                    poly = (A, b8//8, c16//16, n256//256)
                    if survives(*poly):
                        out[poly] = ((d, e, f), (A, u, v, w))
    for m in range(3,94**2//8+1,2):
        if not squarefree(m):continue
        for t in range(2, 24):
            A = 4*t
            # The trace-of-square bound A^2 bounds each coefficient separately.
            U, V = isqrt((A*A-1)//8), isqrt((A*A-1)//(8*m))
            for s, v, w in product(range(-U,U+1), range(-V,V+1), range(-V,V+1)):
                if not v and not w:
                    continue
                h, g = v*v+w*w, v*v-w*w+2*v*w
                B = 6*t*t-4*s*s-4*m*h
                C = 4*t**3-8*t*s*s-8*t*m*h+8*m*s*g
                N = (t*t+2*s*s-2*m*h)**2-2*(2*t*s-m*g)**2
                poly = A, B, C, N
                if survives(*poly):
                    out[poly] = ((m,), (t, s, v, w))
    return out


def embedding_boxes(fld, coords):
    a, b, c, d = coords
    if len(fld) == 3:
        roots = [(isqrt(k*S*S), isqrt(k*S*S)+1) for k in fld]
        vectors = [(b*i,c*j,d*k) for i,j,k in ROOTS]
        shift, den = S*a, 4
    else:
        m, = fld
        r = isqrt(2*S*S)
        roots = [(r,r+1), (isqrt(m*(2*S+r)*S),isqrt(m*(2*S+r+1)*S)+1),
                 (isqrt(m*(2*S-r-1)*S),isqrt(m*(2*S-r)*S)+1)]
        vectors = [(b,c,d),(-b,-d,c),(b,-c,-d),(-b,d,-c)]
        shift, den = S*a, 1
    lo, hi = [], []
    for vector in vectors:
        lo.append((shift+sum(z*r[z<0] for z,r in zip(vector,roots)))//den)
        hi.append(-((-shift-sum(z*r[z>=0] for z,r in zip(vector,roots)))//den))
    j = lo.index(min(lo))
    assert 0 < lo[j] <= hi[j] < S and all(hi[j] < lo[i] for i in range(4) if i != j)
    perm = [i^j if len(fld)==3 else (i+j)%4 for i in range(4)]
    return [lo[i] for i in perm], [hi[i] for i in perm]


def constraints(fld, coords, extra):
    lower, upper = embedding_boxes(fld,coords)
    z = [F(0)]*4
    rows = []; rhs = []
    def add(p, q, bound):
        rows.append([(w*(lower[i] if w>=0 else upper[i])+S*q[i]).__floor__()
                     for i,w in enumerate(p)])
        rhs.append((S*F(bound)).__ceil__())
    add([1]*4, z, 1)
    add(z, [-1]*4, F(-1,2))
    add(z, [1]*4, 1)
    if fld in [(8,28,56),(3,)]:
        qchar=[x[0] for x in ROOTS] if len(fld)==3 else [1,-1,1,-1]
        for sign in (-1,1):add(z,[sign*v-1 for v in qchar],F(-2,94))
    for i in range(1, 4):
        w=z.copy();w[0]=1;w[i]=-1
        add(w,z,0);add(z,w,0)
    if len(fld)==3:
        chars = [(c,[g[i] for g in ROOTS],[0]*4) for i,c in enumerate(fld)]
    else:
        chars = [(16*fld[0],[1,0,-1,0],[0,1,0,-1]),(8,[1,-1,1,-1],[0]*4)]
    for c,re,im in chars:
        phases=[(F(1),F(0)),(F(-1),F(0))]
        if any(im):
            phases+= [(F(0),F(j)) for j in (-1,1)]
            phases+= [(F(i*z,5),F(j*w,5)) for z,w in [(3,4),(4,3)] for i,j in product([-1,1],repeat=2)]
        projections=[[x*j+y*k for j,k in zip(re,im)] for x,y in phases]
        for v in projections:
            for ordinary in (True,False):
                h=gcd(c,2 if ordinary else 4)
                bound=F(isqrt(h*c*S*S)+1,c*S)
                add(v if ordinary else z,z if ordinary else v,bound)
        if extra:
            # Choose a rational minorant of sqrt(c); (sqrt(c)-r) is nonnegative.
            # Norm bound |Q|+... implies 2u r Re(P)+r Re(Q)<=2+u^2
            # only when these real parts have positive combined sign. Otherwise
            # the weakened halfspace follows from its positive right-hand side.
            r=F(isqrt(c*S*S),S)
            for n,p,q in product(range(1,9),projections,projections):
                u=F(n,8);add([2*u*r*x for x in p],[r*x for x in q],2+u*u)
    return rows,rhs


def gap(rows,rhs,weights):
    assert all(type(j) is int and 0<=j<len(rows) and type(w) is int and w>0 for j,w in weights)
    return min(0,min(sum(w*rows[j][i] for j,w in weights) for i in range(4)))-sum(w*rhs[j] for j,w in weights)


def propose(rows,rhs):
    import numpy as np
    from scipy.optimize import linprog
    A=np.asarray(rows,dtype=float)/S;b=np.asarray(rhs,dtype=float)/S
    res=linprog([0]*4+[1],A_ub=np.column_stack((A,-np.ones(len(A)))),b_ub=b,
                bounds=[(0,None)]*4+[(None,None)],method='highs')
    assert res.success
    for scale in (10**6,10**9,10**12):
        weights=[(j,round(-float(x)*scale)) for j,x in enumerate(res.ineqlin.marginals) if -x*scale>.5]
        if gap(rows,rhs,weights)>0:return weights
    return None


def main(make):
    mass_bounds()
    cases=candidates()
    nb=sum(len(fld)==3 for fld,v in cases.values())
    nc=len(cases)-nb
    assert (nb,nc)==(662,74)
    records={} if make else json.loads(FILE.read_text())
    assert make or len(records)==len(cases)
    for poly,(fld,v) in sorted(cases.items()):
        key=','.join(map(str,poly))
        if make:
            for extra in (False,True):
                rows,rhs=constraints(fld,v,extra)
                weights=propose(rows,rhs)
                if weights:
                    records[key]={'mixed':extra,'weights':weights};break
            else:raise AssertionError((poly,fld,v))
        rec=records[key];rows,rhs=constraints(fld,v,rec['mixed'])
        assert gap(rows,rhs,rec['weights'])>0
    if make:FILE.write_text(json.dumps(records,separators=(',',':'))+'\n')
    print(f'PASS: {nb} biquadratic and {nc} cyclic primitive ratios; {sum(r["mixed"] for r in records.values())} mixed certificates.')

if __name__=='__main__':main('--make' in sys.argv[1:])

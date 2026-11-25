"""Verify all primitive quartic exclusions for the five non-half, conductor-12 fields."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import gcd, isqrt
from pathlib import Path
import json
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
CERT = HERE / 'three_nonhalf_duals.json'
SCALE = 10**10
CHARS = ((1,1,-1,-1),(1,-1,1,-1),(1,-1,-1,1))
U, Z = (1,)*4, (0,)*4
FIELDS = [(12,5,60,106),(12,28,21,390),(12,40,120,390),
          (12,44,33,106),(12,13,156,390)]


def candidates():
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        fields = work/'fields.txt'
        rows = work/'elements.txt'
        fields.write_text(''.join(' '.join(map(str,r))+'\n' for r in FIELDS))
        exe = work/'enumerate'
        subprocess.run(['c++','-O3','-std=c++17',str(HERE/'biquadratic.cpp'),'-o',str(exe)],check=True)
        subprocess.run([str(exe),str(fields),str(rows)],check=True)
        return [tuple(map(int,r.split())) for r in rows.read_text().splitlines()]


def basis_bounds(row):
    cs, a, u = row[:3], row[3], row[4:7]
    roots = [isqrt(c*SCALE**2) for c in cs]
    bounds = []
    for i in range(4):
        lo = hi = a*SCALE
        for j in range(3):
            v = CHARS[j][i]*u[j]
            lo += v*(roots[j]+int(v<0))
            hi += v*(roots[j]+int(v>0))
        bounds.append((F(lo,4*SCALE),F(hi,4*SCALE)))
    k = min(range(4), key=lambda i:bounds[i][0])
    assert bounds[k][1]<min(bounds[j][0] for j in range(4) if j!=k)
    return [bounds[i^k] for i in range(4)]


def prep(cs, six_two_fields=False):
    m=[]
    def add(v,w,b): m.append((tuple(map(F,v)),tuple(map(F,w)),F(b)))
    def mul(w,v): return tuple(w*z for z in v)
    def uroot(n,d): return F(isqrt(n*d*SCALE*SCALE)+1,d*SCALE)
    for j in range(1,4):
        e = tuple(int(i==0)-int(i==j) for i in range(4))
        add(e,Z,0)
        add(Z,e,0)
    add(U,mul(-1,U),0)
    add(U,Z,1)
    add(mul(-1,U),Z,-(F(1,2) if six_two_fields else F(1,3)))
    add(Z,U,1)
    add(Z,mul(-1,U),-(F(5,8) if six_two_fields else (F(3,5) if cs[1] in (5,44) else F(7,12))))
    if 5 not in cs and not six_two_fields:
        add(mul(-1,U),mul(-2,U),F(-5,3))
    for c,v in zip(cs,CHARS):
        root=F(isqrt(c*SCALE*SCALE),SCALE)
        for sign in (-1,1):
            add(mul(sign,v),Z,uroot(gcd(c,2),c))
            add(Z,mul(sign,v),uroot(gcd(c,4),c))
            for n in range(-16,17):
                r=F(n,32)
                # For a negative projected signed coefficient, this weakened
                # mixed inequality also follows from c*(2*r*u-r^2)<=2.
                add(mul(2*c*r,v),mul(sign*root,v),2+c*r*r)
        for x,y in product(range(-3,4),repeat=2):
            if gcd(x,y)==1:
                add(mul(x,v),mul(y,v),uroot(2*x*x+4*y*y,c))
    return m


def constraints(row, base):
    roots=basis_bounds(row)
    out=[]
    for p,q,b in base:
        v=[(p[i]*roots[i][p[i]<0]+q[i])*SCALE for i in range(4)]
        out.append(([x.__floor__() for x in v],(b*SCALE).__ceil__()))
    for j in range(1,4):
        out.append(([(SCALE*(roots[i][0]-roots[i^j][1])).__floor__() for i in range(4)],0))
    return out


def gap(rows,w):
    assert all(type(j) is int and type(k) is int and 0<=j<len(rows) and k>0 for j,k in w)
    # The true q_i are nonnegative and have sum <=1; subtracting a common
    # constant accounts for this normalization without a separate variable.
    low=min(0,min(sum(k*rows[j][0][i] for j,k in w) for i in range(4)))
    return low-sum(k*rows[j][1] for j,k in w)


def run(generate):
    if generate:
        import numpy as np
        from scipy.optimize import linprog
        records=[]
    else:
        records=json.loads(CERT.read_text())
    data=candidates()
    assert Counter(row[:3] for row in data)=={r[:3]:n for r,n in zip(FIELDS,(168,321,108,16,139))}
    assert generate or len(records)==len(data)
    cache={r[:3]:prep(r[:3]) for r in FIELDS}
    least=None
    for n,row in enumerate(data):
        rs=constraints(row,cache[row[:3]])
        if generate:
            a=np.array([r for r,b in rs],float)/SCALE
            b=np.array([b for r,b in rs],float)/SCALE
            result=linprog([0]*4+[1],A_ub=np.column_stack([a,-np.ones(len(a))]),b_ub=b)
            assert result.success and result.fun>1e-9,(row,result)
            rec=[[j,round(-v*10**12)] for j,v in enumerate(result.ineqlin.marginals) if -v*10**12>=1]
            records.append(rec)
        g=gap(rs,records[n]); assert g>0,(row,g)
        least=min(least,g) if least is not None else g
    if generate: CERT.write_text(json.dumps(records,separators=(',',':'))+'\n')
    print('primitive ratio orbits excluded',len(data),'minimum exact gap',least)

if __name__=='__main__':
    run('--generate' in sys.argv)

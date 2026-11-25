"""Exact field, moment and Fourier certificates for every quartic conductor-20 branch."""
from fractions import Fraction as F
from itertools import product
from math import isqrt,gcd
from pathlib import Path
import json
import subprocess
import sys
import tempfile
from three_nonhalf import gap
from c20_bound import bound

D=Path(__file__).resolve().parent
Z=(0,0,0,0); O=(1,1,1,1); S=10**10
CASES = [
    ('high', 398, F(1, 3), F(23, 36), 0),
    ('irr', 117, F(1, 2), F(2, 3), 0),
    ('half', 77, F(1, 2), F(1, 2), F(1, 2)),
    ('gold', 77, F(1, 2), F(1, 2), F(1, 2)),
    ('eleven', 77, F(11, 20), F(11, 20), F(11, 20)),
    ('three', 77, F(3, 5), F(3, 5), F(3, 5)),
]
CERT=D/'c20_duals.json'

def bnds(scale):
    z=isqrt(5*scale*scale)
    p=isqrt((5*scale+z)*scale//2)
    m=isqrt((5*scale-z-1)*scale//2)
    return [(F(p,scale),F(p+2,scale)),(F(m,scale),F(m+2,scale)),
            (F(-p-2,scale),F(-p,scale)),(F(-m-2,scale),F(-m,scale))]

def roots(r):
    a,b,c,d,*_=r
    out=[]
    for lo,hi in bnds(10**14):
        x=y=F(d)
        for v in (c,b,a):
            w=[lo*x,lo*y,hi*x,hi*y]
            x,y=v+min(w),v+max(w)
        out.append(((x*S).__floor__(),(y*S).__ceil__()))
    i=min(range(4),key=lambda i:out[i][0]);out=out[i:]+out[:i]
    assert 0<out[0][0]<out[0][1]<S and all(out[0][1]<l for l,h in out[1:])
    return out

def candidates():
    # Check the constants in cyclic20.cpp independently using nested radicals.
    yl,yh=bnds(10**18)[0]
    for j,expect in enumerate((1902113032,3618033988,6881909602),1):
        assert (yl**j*10**9).__floor__()==(yh**j*10**9).__floor__()==expect
    with tempfile.TemporaryDirectory() as tmp:
        exe=Path(tmp)/'enum';subprocess.run(['c++','-O3','-std=c++17',str(D/'cyclic20.cpp'),'-o',str(exe)],check=True)
        output=subprocess.check_output([str(exe),'398'],text=True).splitlines()
    ans={}
    for line in output:
        r=tuple(map(int,line.split()));ans[r[4:]]=r
    assert len(output)==908 and len(ans)==721
    return [ans[p] for p in sorted(ans)]

def neg(v):return tuple(-z for z in v)
def mul(x,v):return tuple(x*z for z in v)
def uroot(n,d):return F(isqrt(n*d*S*S)+1,d*S)
def base(case):
    name,lim,s,t,k=case
    rows=[]
    def add(p,q,b):
        rows.append((tuple((F(z)*S).__floor__() for z in p),tuple((F(z)*S).__floor__() for z in q),(F(b)*S).__ceil__()))
    for j in range(1,4):
        e=tuple(int(i==0)-int(i==j) for i in range(4));add(e,Z,0);add(Z,e,0)
    if name!='irr':add(O,neg(O),0)
    add(neg(O),Z,-s);add(Z,neg(O),-t);add(O,Z,s if k else 1);add(Z,O,t if k else 1)
    add(neg(O),neg(O),-1)
    if name=='gold':
        z=(1,-1,1,-1);add(Z,z,uroot(1,10));add(Z,neg(z),uroot(1,10))
    for c,f in [(5,2),(20,1)]:
        d={(F(1),F(0)),(F(0),F(1)),(F(3,5),F(4,5)),(F(4,5),F(3,5)),(F(7,10),F(7,10))}
        d=set((a*x,b*y) for a,b in d for x,y in product((-1,1),repeat=2))
        planes=sorted(set(tuple((x,y,-x,-y)[(f*i)%4] for i in range(4)) for x,y in d))
        root=F(isqrt(c*S*S),S)
        for v in planes:
            add(v,Z,uroot(gcd(c,2),c));add(Z,v,uroot(gcd(c,4),c))
            for w in planes:
                for n in range(1,6):
                    r=F(n,16);add(mul(2*c*r,v),mul(root,w),2+c*r*r)
    return rows

def rows(x,case,base):
    name,cap,s,t,k=case
    rr=[([p[i]*x[i][p[i]<0]//S+q[i] for i in range(4)],b) for p,q,b in base]
    for j in ((2,) if name=='irr' else (1,2,3)):
        rr.append(([x[i][0]-x[(i+j)%4][1] for i in range(4)],0))
    if k:
        for j in (1,2,3):
            rr.append(([-((x[i][1]*x[(i+j)%4][1]+S-1)//S) for i in range(4)],(-k*S).__ceil__()))
    return rr

def run(generate=False):
    if generate:
        import numpy as np
        from scipy.optimize import linprog
        records=[]
    else:
        records=json.loads(CERT.read_text())
    data=candidates()
    bases={case[0]:base(case) for case in CASES}
    idx=0;total={}
    for case in CASES:
        name,cap,s,t,k=case;tested=0
        for r in data:
            a,b,c,n=r[4:]
            if a>cap:continue
            if k and name != 'gold':
                # Rational signed complements and equal mass give
                # P(X) = (X-1)^4 modulo the denominator of t.
                if any((coefficient-target) % t.denominator
                       for coefficient,target in zip((a,b,c,n), (4,6,4,1))):
                    continue
            rs=rows(roots(r),case,bases[name])
            if generate:
                A=np.array([v for v,z in rs],float)/S; B=np.array([z for v,z in rs],float)/S
                sol=linprog([0]*4+[1],A_ub=np.column_stack([A,-np.ones(len(A))]),b_ub=B)
                assert sol.success and sol.fun>1e-9,(case,r,sol.fun)
                weights=[[j,round(-w*10**12)] for j,w in enumerate(sol.ineqlin.marginals) if -w*10**12>=1]
                records.append(weights)
            assert gap(rs,records[idx])>0,(case,r)
            idx+=1;tested+=1
        total[name]=tested
    if generate:CERT.write_text(json.dumps(records,separators=(',',':'))+'\n')
    assert len(records)==idx
    print('cyclic conductor 20',total,'total exact exclusions',idx)

if __name__=='__main__':run('--generate' in sys.argv)

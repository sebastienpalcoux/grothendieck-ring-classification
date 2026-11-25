"""Certificates for the rational and bounded irrational parts of Q(sqrt2,sqrt5)."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from three_nonhalf import F,SCALE,CHARS,basis_bounds,prep,gap
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from verify_quartic_half_ten import moments, roots
HERE=Path(__file__).resolve().parent
CERT=HERE/'silvergold_duals.json'
CS=(8,5,40)
def enum():
    with tempfile.TemporaryDirectory() as t:
        w=Path(t);exe=w/'enum';f=w/'fields';o=w/'out';f.write_text('8 5 40 550\n')
        subprocess.run(['c++','-O3','-std=c++17',str(HERE/'biquadratic.cpp'),'-o',str(exe)],check=True)
        subprocess.run([str(exe),str(f),str(o)],check=True)
        return [tuple(map(int,x.split())) for x in o.read_text().splitlines()]

def constraints(r,irr=0,smin=F(2,5),tmin=F(23,36),sm=None,tm=None,cut=None,ordbound=None,swap_mom=None,qfive=None):
    xs=basis_bounds(r);base=STANDARD.copy()
    def add(p,q,v):base.append((p,q,v))
    O=(1,)*4;M=(-1,)*4;Z=(0,)*4
    if irr==0:add(O,M,0)
    add(M,Z,-smin);add(Z,M,-tmin)
    if irr==0 or smin+tmin>=1:add(M,M,-1)
    if sm is not None:add(O,Z,sm);add(M,Z,-sm)
    if tm is not None:add(Z,O,tm);add(Z,M,-tm)
    if irr==8:
        for e in (-1,1):add(Z,tuple(e*x-1 for x in CHARS[0]),F(-2,94))
    if sm==F(2,5) and irr:
        for e in (-1,1):
            z=tuple(e*x for x in CHARS[1]);add(z,Z,0);add(Z,z,0)
    if qfive is not None:
        for e in (-1,1):add(Z,tuple(e*x for x in CHARS[1]),qfive)
    if ordbound is not None:
        for e in (-1,1):add(tuple(e*x for x in CHARS[1]),Z,ordbound)
    rr=[([(SCALE*(p[i]*xs[i][p[i]<0]+q[i])).__floor__() for i in range(4)],
          (SCALE*F(v)).__ceil__()) for p,q,v in base]
    for j in ((1,2,3) if not irr else (CS.index(irr)+1,)):
        rr.append(([(SCALE*(xs[i][0]-xs[i^j][1])).__floor__() for i in range(4)],0))
    if cut is not None:
        for j in (1,2,3):rr.append(([(-SCALE*xs[i][1]*xs[i^j][1]).__floor__() for i in range(4)],(-SCALE*cut).__ceil__()))
    if swap_mom is not None:
        first,second=swap_mom
        for j in (1,3):
            rr.append(([(-SCALE*xs[i^j][1]).__floor__() for i in range(4)],(-SCALE*first).__ceil__()))
            rr.append(([(-SCALE*xs[i][1]*xs[i^j][1]).__floor__() for i in range(4)],(-SCALE*second).__ceil__()))
    return rr

orig=prep(CS,True)
STANDARD=orig[:6]+[orig[7],orig[9]]+orig[11:]

def run(generate=False):
    if generate:
        import numpy as np
        from scipy.optimize import linprog
        rec=[]
    else:rec=json.loads(CERT.read_text())
    idx=0;ct={}
    def disc(r,kw,optional=False):
        nonlocal idx
        rs=constraints(r,**kw)
        if generate:
            a=np.array([q for q,b in rs],float)/SCALE;b=np.array([b for q,b in rs],float)/SCALE
            sol=linprog([0]*4+[1],A_ub=np.column_stack([a,-np.ones(len(a))]),b_ub=b)
            assert sol.success
            w=[[j,round(-z*10**12)] for j,z in enumerate(sol.ineqlin.marginals) if -z*10**12>=1]
            if not w or gap(rs,w)<=0:
                assert optional,(r,kw,sol.fun)
                w=[]
            rec.append(w)
        w=rec[idx];idx+=1
        if not w:assert optional;return False
        assert gap(rs,w)>0,(r,kw);return True
    data=enum();assert len(data)==594
    strag=[]
    for r in data:
        if not disc(r,{},True):strag.append(r)
    assert [r[3] for r in strag]==[64,166]
    for r in strag:
        disc(r,dict(tmin=F(18,25)))
        for s in (F(4,7),F(5,7)):disc(r,dict(sm=s,tm=F(5,7)))
        for h in (9,16,25):
            t=F(3,4)-F(1,h)
            for b in range(1,h//4+1):
                s=F(3,4)-F(b,h);c=F(1,4)+F(b*b,h)
                if s in (F(19,36),F(9,16),F(59,100)):
                    continue
                disc(r,dict(sm=s,tm=t,cut=int(1+c)-c))
    for fld,t,cap in [(8,F(1,2),94),(40,F(3,4),94),(5,F(2,3),94),(5,F(143,200),510)]:
        small=[r for r in data if r[3]<=cap]
        for r in small:
            disc(r,dict(irr=fld,smin=F(1,2),tmin=t))
        ct[fld,str(t)]=len(small)

    # Record counts after positivity, after the simultaneous minimum,
    # and after the Fourier and shifted-moment conditions.
    expected={
        False: {(16,62,64,1):(15,0,0),(32,254,368,1):(197,0,0)},
        True: {(14,47,26,1):(15,0,0),(18,43,18,1):(23,1,0)},
    }
    for golden,cap in ((False,38),(True,24)):
        counts={}
        for r in data:
            poly=(r[3],*r[-3:])
            a,b,c,h=poly
            if a<=cap and not a%2 and not c%2 and b%2==golden and h%2:
                counts[poly]=moments(poly,'biquadratic',weight_cap=F(39,50),golden_unit=golden)
        assert counts==expected[golden]
        print('golden' if golden else 'rational', 'trace cap',cap,'moment counts',counts)

    # The one vector satisfying the minimum has moments 1,1,6,81.
    # Its weights are the residues of the unique rational function
    # matching these four coefficients in the expansion at infinity.
    weights=[]
    for lo,hi in roots((18,43,18,1)):
        top=(lo**3-17*hi**2+31*lo-2,hi**3-17*lo**2+31*hi-2)
        bot=(4*lo**3-54*hi**2+86*lo-18,4*hi**3-54*lo**2+86*hi-18)
        assert bot[0]*bot[1]>0
        vals=[v/w for v in top for w in bot]
        weights.append((min(vals),max(vals)))
    assert all(v[0]>0 for v in weights)
    assert all(weights[0][1]<v[0] for v in weights[1:])
    assert max(v[0] for v in weights)>F(85,100)
    print('exceptional moment pair (6,81), largest normalized weight > 0.85')
    if generate:CERT.write_text(json.dumps(rec,separators=(',',':'))+'\n')
    assert idx==len(rec)
    print('Q(sqrt2,sqrt5): exact Fourier separations',idx-2,'irrational branch counts',ct)
if __name__=='__main__':run('--generate' in sys.argv)

"""Conductor 40: exact separating weights and integral trace lattices."""
from fractions import Fraction as F
from pathlib import Path
import json,sys
from units import census, proper_dimension_height
import sympy as sp
from sympy.matrices.normalforms import hermite_normal_form
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'quartic_more/biquadratic.cpp').exists())
sys.path.insert(0,str(ROOT/'quartic_more'))
from silvergold import CHARS,SCALE,constraints,gap
CERT=HERE/'duals.json'

def mul(a,b):
    # The two independent basis relations are r^2=2 and phi^2=1+phi.
    out=[0]*4
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            index=(i^j)&1;factor=x*y*(2 if i&j&1 else 1);power=(i>>1)+(j>>1)
            if power!=1:out[index]+=factor
            if power!=0:out[index+2]+=factor
    return sp.Matrix(out)

def difference_lattice(row):
    d,e,f,A,u,v,w,*_=row
    xs=[]
    for a,b in ((1,1),(1,-1),(-1,1),(-1,-1)):
        assert (A-b*v)%4==0 and (a*u-a*b*w)%2==0 and v%2==0
        xs.append(sp.Matrix([(A-b*v)//4,(a*u-a*b*w)//2,b*v//2,a*b*w]))
    lattice=hermite_normal_form(sp.Matrix.hstack(*[xs[i]-xs[i^2] for i in range(4)]))
    while True:
        new=hermite_normal_form(sp.Matrix.hstack(lattice,*[mul(x,v) for x in xs for v in lattice.columnspace()]))
        if new==lattice:return lattice
        lattice=new

def separating(rows):
    import numpy as np
    from scipy.optimize import linprog
    m=np.array([x for x,b in rows],float)/SCALE;b=np.array([b for x,b in rows],float)/SCALE
    opt=linprog([0]*4+[1],A_ub=np.column_stack([m,-np.ones(len(m))]),b_ub=b,bounds=[(0,None)]*4+[(None,None)])
    assert opt.success
    if opt.fun<1e-9:return []
    w=[[i,round(-z*10**12)] for i,z in enumerate(opt.ineqlin.marginals) if -z*10**12>.5]
    assert gap(rows,w)>0
    return w

def run(generate):
    proper_dimension_height()
    ratios=census();assert len(ratios)==1065
    data=[] if generate else json.loads(CERT.read_text());idx=0;unresolved=[]
    def check(rows,may=False):
        nonlocal idx
        w=separating(rows) if generate else data[idx]
        if generate:data.append(w)
        idx+=1
        if not w:assert may;return False
        assert gap(rows,w)>0
        return True
    for row in ratios:
        if row[3]<=94:continue
        rows=constraints(row,irr=5,smin=F(1,2),tmin=F(6837,10000),qfive=F(21,100))
        if not check(rows,True):unresolved.append(row)
    assert [r[3] for r in unresolved]==[166,564]
    for row in unresolved:
        lattice=difference_lattice(row)
        if row[3]==564:
            assert lattice==sp.diag(4,2,4,2)
            assert F(6837,10000)*4>2 and F(143,200)*4<3
            continue
        assert lattice==sp.diag(16,4,16,4)
        assert 10<16*F(6837,10000)<11<16*F(143,200)<12
        base=constraints(row,irr=5,smin=F(1,2),tmin=F(6837,10000),tm=F(11,16),qfive=F(21,100))
        for sign,bound in ((1,F(-7,10)),(-1,F(54,100))):
            check(base+[([sign*x*SCALE for x in CHARS[0]],(bound*SCALE).__ceil__())])
    assert len(data)==idx
    if generate:CERT.write_text(json.dumps(data,separators=(',',':'))+'\n')
    print('1065 primitive ratios; 2 integral trace lattices;',idx-2,'strict rational separation certificates.')

if __name__=='__main__':run('--generate' in sys.argv)

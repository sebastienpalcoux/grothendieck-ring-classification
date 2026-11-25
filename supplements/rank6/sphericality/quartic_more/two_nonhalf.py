"""The five remaining conductor-eight fields, away from half mass."""
from collections import Counter
from itertools import product
import json
import tempfile
import subprocess
import sys
from three_nonhalf import F, SCALE, HERE, basis_bounds, constraints, gap, prep, isqrt

FIELDS=[(8,28,56,397),(8,44,88,128),(8,13,104,230),(8,17,136,128),
        (8,60,120,128),(8,76,152,128),(8,21,168,128),(8,92,184,128),
        (8,29,232,128),(8,33,264,128),(8,37,296,128),(8,41,328,128)]
CYCLIC=[(8,16*m,2,1,1,m,1,128) for m in (3,5,7)]
CERT=HERE/'two_nonhalf_duals.json'


def candidates():
    out=[]
    for rows,name in [(FIELDS,'biquadratic'),(CYCLIC,'cyclic')]:
        with tempfile.TemporaryDirectory() as tmp:
            from pathlib import Path
            w=Path(tmp);exe=w/'enum';inp=w/'fields';data=w/'elements'
            inp.write_text(''.join(' '.join(map(str,x))+'\n' for x in rows))
            subprocess.run(['c++','-O3','-std=c++17',str(HERE/(name+'.cpp')),'-o',str(exe)],check=True)
            subprocess.run([str(exe),str(inp),str(data)],check=True)
            out.extend([tuple(map(int,x.split())) for x in data.read_text().splitlines()])
    return out


def cybounds(row):
    a,J,d,b,c,m,I,A,u,v,w,B,C,N=row
    assert (a,J,d,b,c,I)==(8,16*m,2,1,1,1)
    r=isqrt(2*SCALE*SCALE)
    ylo=isqrt(m*(2*SCALE+r)*SCALE)
    yhi=isqrt(m*(2*SCALE+r+1)*SCALE)+1
    zlo=isqrt(m*(2*SCALE-r-1)*SCALE)
    zhi=isqrt(m*(2*SCALE-r)*SCALE)+1
    out=[]
    for h,j,k in [(u,v,w),(-u,-w,v),(u,-v,-w),(-u,w,-v)]:
        lo=hi=F(A,4)
        for coef,x,y in [(F(h,2),r,r+1),(j,ylo,yhi),(k,zlo,zhi)]:
            lo+=F(coef*([x,y][coef<0]),SCALE);hi+=F(coef*([y,x][coef<0]),SCALE)
        out.append((lo,hi))
    z=min(range(4),key=lambda i:out[i][0])
    assert all(i==z or out[z][1]<out[i][0] for i in range(4))
    return out[z:]+out[:z]


def cyrows(row,base):
    # prep((8,)) has a biquadratic character row with signs +,+,-,-;
    # replacing it by the cyclic order-two character only permutes entries.
    roots=cybounds(row)
    out=[]
    for nn,(p,q,b) in enumerate(base):
        if nn>=11:
            p=tuple(p[i] for i in [0,2,1,3]);q=tuple(q[i] for i in [0,2,1,3])
        out.append(([(SCALE*(p[i]*roots[i][p[i]<0]+q[i])).__floor__() for i in range(4)],
                    (b*SCALE).__ceil__()))
    for j in range(1,4):
        out.append(([(SCALE*(roots[i][0]-roots[(i+j)%4][1])).__floor__() for i in range(4)],0))
    dirs={(F(1),F(0)),(F(0),F(1)),(F(3,5),F(4,5)),(F(4,5),F(3,5)),(F(7,10),F(7,10))}
    dirs=list(set((x*s,y*t) for x,y in dirs for s,t in product((-1,1),repeat=2)))
    J=row[1];cl=F(isqrt(J*SCALE*SCALE),SCALE)
    def add(v,w,b):
        out.append(([(SCALE*(v[i]*roots[i][v[i]<0]+w[i])).__floor__() for i in range(4)],(SCALE*b).__ceil__()))
    for x,y in dirs:
        v=(x,y,-x,-y)
        add(v,[0]*4,F(isqrt(2*J*SCALE*SCALE)+1,J*SCALE))
        add([0]*4,v,F(isqrt(4*J*SCALE*SCALE)+1,J*SCALE))
        for z,t in dirs:
            w=(z,t,-z,-t)
            for rn in (1,2,3,4):
                r=F(rn,16)
                add([2*J*r*h for h in v],[cl*h for h in w],2+J*r*r)
    return out


def run(generate=False):
    if generate:
        import numpy as np
        from scipy.optimize import linprog
        records=[]
    else:records=json.loads(CERT.read_text())
    data=candidates();count=Counter(tuple(r[:3]) if len(r)==10 else r[:2] for r in data)
    print('field counts', dict(count))
    assert generate or len(records)==len(data)
    bases={r[:3]:prep(r[:3],True) for r in FIELDS};cb=prep((8,),True)
    least=None
    for n,row in enumerate(data):
        rs=constraints(row,bases[row[:3]]) if len(row)==10 else cyrows(row,cb)
        if generate:
            a=np.array([r for r,b in rs],float)/SCALE;b=np.array([b for r,b in rs],float)/SCALE
            z=linprog([0]*4+[1],A_ub=np.column_stack([a,-np.ones(len(a))]),b_ub=b)
            assert z.success and z.fun>1e-9,(row,z.fun)
            records.append([[j,round(-w*10**12)] for j,w in enumerate(z.ineqlin.marginals) if -w*10**12>=1])
        v=gap(rs,records[n]);assert v>0,(row,v)
        least=min(least,v) if least is not None else v
    if generate:CERT.write_text(json.dumps(records,separators=(',',':'))+'\n')
    print('primitive ratios excluded',len(data),'minimum exact gap',least)

if __name__=='__main__':run('--generate' in sys.argv)

"""Finite all-word unit-functional congruences on a complete candidate domain.

This checks integrality only. Nonnegativity of monomials and existence of a
based fusion ring are separate necessary conditions.
"""
import argparse
import hashlib
import json
import math
import time
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from flint import fmpz_mat

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def require(value,message):
    if not value:raise RuntimeError(message)

def digest(value):return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()

def qm(x,y):return (x[0]*y[0]+x[1]*y[1],x[0]*y[1]+x[1]*y[0]+x[1]*y[1])
def mul(x,y):
    if len(x)==2:return qm(x,y)
    a=qm(x[:2],y[:2]);b=qm(x[2:],y[2:]);c=qm(x[:2],y[2:]);d=qm(x[2:],y[:2])
    return (a[0]-2*b[0],a[1]-2*b[1],c[0]+d[0],c[1]+d[1])
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def scale(n,x):return tuple(n*a for a in x)
def qinv(x):
    norm=x[0]*x[0]+x[0]*x[1]-x[1]*x[1]
    require(norm!=0,'Zero divisor in quadratic denominator.')
    return (F(x[0]+x[1],norm),F(-x[1],norm))
def trace(x):return 2*x[0]+x[1] if len(x)==2 else 4*x[0]+2*x[1]

def source(rid):
    require(rid in ('R7_5_3895','R7_5_5039'),'Unsupported source tensor.')
    degree=2 if rid.endswith('3895') else 4
    def q(a=0,b=0):return (a,b)+(0,)*(degree-2)
    def dims(a,b):return q(a-b,2*b)
    zero=q();one=q(1);phi=q(0,1);phibar=q(1,-1)
    avec=[1,5,5,10,8,8,9] if degree==2 else [1,5,5,8,8,10,9]
    bvec=[0,2,2,4,4,4,4]
    ds=[dims(a,b) for a,b in zip(avec,bvec)]
    bars=[dims(a,-b) for a,b in zip(avec,bvec)]
    D=q(400,640);Dbar=q(1040,-640)
    if degree==2:
        chars=[[q(x) for x in [1,-1,-1,0,0,0,1]],
               [q(x) for x in [1,-1,3,-2,0,0,1]],
               [q(x) for x in [1,3,-1,-2,0,0,1]],bars,ds,
               [one,zero,zero,zero,phi,phibar,q(-1)],
               [one,zero,zero,zero,phibar,phi,q(-1)]]
        fs=[q(4),q(16),q(16),Dbar,D,q(5),q(5)]
    else:
        gamma=(0,0,1,0)
        chars=[[q(x) for x in [1,1,1,0,0,-2,1]],bars,ds,
               [one,add(q(-1),gamma),add(q(-1),scale(-1,gamma)),zero,zero,zero,one],
               [one,add(q(-1),scale(-1,gamma)),add(q(-1),gamma),zero,zero,zero,one],
               [one,zero,zero,phi,phibar,zero,q(-1)],
               [one,zero,zero,phibar,phi,zero,q(-1)]]
        fs=[q(8),Dbar,D,q(8),q(8),q(5),q(5)]
    census=json.loads((ROOT/'supplements/rank7/output/m5/census.json').read_text())
    N=next(r['tensor'] for r in census if r['id']==rid)
    dual=[next(j for j in range(7) if N[i][j][0]) for i in range(7)]
    for row,f in zip(chars,fs):
        for i in range(7):
            for j in range(7):
                expected=tuple(sum(N[i][j][k]*row[k][h] for k in range(7)) for h in range(degree))
                require(mul(row[i],row[j])==expected,'Raw-tensor character identity failed.')
        require(tuple(sum(mul(row[i],row[dual[i]])[h] for i in range(7)) for h in range(degree))==f,
                'Formal codegree identity failed.')
    require(tuple(sum(mul(z,z)[h] for z in ds) for h in range(degree))==D,'Global dimension failed.')
    return degree,ds,D,chars,fs,digest(N)

def domain(data):
    degree,ds,D,chars,fs,source_hash=source(data['id'])
    one=(1,)+(0,)*(degree-1)
    low=[(1,0,0,0,0,0,0)]+[tuple(v) for v in data['low']]
    orbits=[[(0,)+tuple(v) for v,gram,z in orbit] for orbit in data['orbits']]
    rows=sorted(set(low+sum(orbits,[])))
    points=[];point_index={};rowdata={}
    for v in rows:
        z=tuple(sum(v[i]*ds[i][h] for i in range(7)) for h in range(degree))
        require(not any(z[2:]),'A center dimension left the real quadratic field.')
        eigen=[]
        for char,f in zip(chars,fs):
            value=tuple(sum(v[i]*char[i][h] for i in range(7)) for h in range(degree))
            den=qm(f[:2],z[:2]);recip=qinv(den)+(0,)*(degree-2)
            lam=mul(mul(D,value),recip)
            require(all(F(x).denominator==1 for x in lam),
                    'The supplied candidate domain contains a nonintegral central eigenvalue: '+str(v))
            eigen.append(tuple(int(x) for x in lam))
        signature=tuple(eigen)
        if signature not in point_index:
            point_index[signature]=len(points);points.append(signature)
        # 6400*z^2/D^2 = z^2*(13-8phi)^2.
        wt=mul(mul(z,z),(233,-144)+(0,)*(degree-2))
        require(all(F(x).denominator==1 for x in wt),'The normalized weight is not integral after scaling6400.')
        rowdata[v]=(point_index[signature],tuple(int(x) for x in wt))
    # Explicitly verify rationality of every integer-word trace on each
    # individual multiplicity orbit, rather than assume unsigned transport.
    def conjugate(x,kind):
        if kind=='real':
            return tuple(y for a,b in zip(x[::2],x[1::2]) for y in (a+b,-b))
        return tuple(x[:2])+tuple(-a for a in x[2:])
    def record(v):
        point,weight=rowdata[v]
        return (points[point],weight)
    for bundle in [low]+orbits:
        actual=sorted(record(v) for v in bundle)
        for kind in (['real'] if degree==2 else ['real','imaginary']):
            changed=sorted((tuple(conjugate(e,kind) for e in spectrum),conjugate(weight,kind))
                           for spectrum,weight in actual)
            require(changed==actual,'A weighted spectral orbit is not Galois-complete.')

    generators=[]
    for E in range(7):
        gen=[x for point in points for x in point[E]]
        unit=[x for _ in points for x in one]
        if gen!=unit and gen not in generators:generators.append(gen)
    return degree,source_hash,points,generators,rowdata,low,orbits

def bezout(a,b):
    old_r,r=a,b;old_s,s=1,0;old_t,t=0,1
    while r:
        q=old_r//r
        old_r,r=r,old_r-q*r;old_s,s=s,old_s-q*s;old_t,t=t,old_t-q*t
    return old_r,old_s,old_t

def hnf(rows,n,modulus=None):
    if modulus is None:
        matrix=fmpz_mat(rows).hnf()
        require(matrix.ncols()==n and matrix.nrows()>=n,'Unexpected HNF shape.')
        return [[int(matrix[i,j]) for j in range(n)] for i in range(n)]
    # Row-HNF in a lattice containing modulus*Z^n. Insertion uses Bezout
    # operations and reductions by the untouched later ambient vectors.
    # All arithmetic remains bounded; no rational/heuristic lattice routine.
    require(modulus**3*8 < 2**63,'Modular HNF exceeds int64 arithmetic bound.')
    H=np.eye(n,dtype=np.int64)*modulus
    for row in rows:
        v=np.array([int(x)%modulus for x in row],dtype=np.int64)
        for i in range(n):
            if not v[i]:continue
            a=int(H[i,i]);q,r=divmod(int(v[i]),a)
            if q:v[i:]=(v[i:]-q*H[i,i:])%modulus
            if not r:continue
            g,s,t=bezout(a,r);old=H[i,i:].copy();cur=v[i:].copy()
            H[i,i:]=(s*old+t*cur)%modulus;H[i,i]=g
            v[i:]=((-r//g)*old+(a//g)*cur)%modulus
        require(not np.any(v),'Modular HNF insertion left a residual.')
    for j in range(n):
        quot=H[:j,j]//H[j,j]
        H[:j,j:]-=quot[:,None]*H[j,j:]
        H[:j,j:]%=modulus
    return H.tolist()

def products(rows,gen,degree,modulus):
    H=np.array(rows,dtype=np.int64).reshape(len(rows),-1,degree)
    G=np.array(gen,dtype=np.int64).reshape(-1,degree)%modulus
    def qmul(a,b,c,d):return a*c+b*d,a*d+b*c+b*d
    a,b=qmul(H[:,:,0],H[:,:,1],G[:,0],G[:,1])
    if degree==2:out=np.stack((a,b),axis=2)
    else:
        c,d=qmul(H[:,:,2],H[:,:,3],G[:,2],G[:,3])
        e,f=qmul(H[:,:,0],H[:,:,1],G[:,2],G[:,3])
        g,h=qmul(H[:,:,2],H[:,:,3],G[:,0],G[:,1])
        out=np.stack((a-2*c,b-2*d,e+g,f+h),axis=2)
    return (out.reshape(len(rows),-1)%modulus).tolist()

def index_exponents(H):
    out={2:0,5:0}
    for i,row in enumerate(H):
        value=row[i]
        require(value>0,'HNF diagonal is not positive.')
        for p in out:
            while value%p==0:out[p]+=1;value//=p
        require(value==1,'Unexpected prime in the modular lattice index.')
    return {str(p):a for p,a in out.items()}

def generate(data,max_rounds=40):
    start=time.monotonic()
    degree,source_hash,points,gens,rowdata,low,orbits=domain(data)
    modulus=6400*degree;n=degree*len(points)
    diag=[[modulus*int(i==j) for j in range(n)] for i in range(n)]
    unit=[int(j%degree==0) for j in range(n)]
    print(json.dumps({"event":"starting_domain","ambient_dimension":n}),flush=True)
    H=hnf([unit]+gens,n,modulus)
    steps=[];complete=False
    print(json.dumps({'event':'domain','id':data['id'],'orbits':len(orbits),'distinct_rows':len(rowdata),
                      'spectral_points':len(points),'ambient_dimension':n,'modulus':modulus}),flush=True)
    for iteration in range(max_rounds):
        active=[[x%modulus for x in row] for row in H if any(x%modulus for x in row)]
        augmented=H[:]
        for gen in gens:augmented.extend(products(active,gen,degree,modulus))
        nxt=hnf(augmented,n,modulus)
        rec={'round':iteration+1,'active_basis':len(active),'index':index_exponents(nxt),
             'lattice_sha256':digest(nxt),'seconds':time.monotonic()-start}
        steps.append(rec);print(json.dumps(rec),flush=True)
        if nxt==H:complete=True;H=nxt;break
        H=nxt
    # Apply the rational projection Tr/[K:Q]; genuine word traces are rational
    # on complete source-Galois/duality orbits. The ambient modulus contributes
    # only integers to this rational functional for every multiplicity vector.
    def coefficient(h,rows):
        total=0
        for v in rows:
            point,weight=rowdata[v]
            total+=trace(mul(weight,tuple(h[degree*point:degree*(point+1)])))
        return int(total)%modulus
    raw=[]
    for h in H:
        if not any(x%modulus for x in h):continue
        raw.append([coefficient(h,low)]+[coefficient(h,orbit) for orbit in orbits])
    variables=1+len(orbits)
    dualdiag=[[modulus*int(i==j) for j in range(variables)] for i in range(variables)]
    reduced=hnf(raw,variables,modulus)
    constraints=[]
    for vector in reduced:
        vector=[x%modulus for x in vector]
        if not any(vector):continue
        g=math.gcd(modulus,*vector[1:])
        if vector[0]%g:
            constraints.append({'modulus':g,'constant':vector[0]%g,'coefficients':[0]*len(orbits),
                                'domain_contradiction':True});continue
        m=modulus//g
        if m==1:continue
        constraints.append({'modulus':m,'constant':(vector[0]//g)%m,
                            'coefficients':[(x//g)%m for x in vector[1:]]})
    return {'id':data['id'],'status':'STABILIZED' if complete else 'PARTIAL',
            'scope':'Necessary all-word unit-multiplicity integrality; no positivity or categorification claim.',
            'source_sha256':source_hash,'domain_sha256':digest({'low':data['low'],'orbits':data['orbits']}),
            'degree':degree,'ambient_modulus':modulus,'spectral_points':len(points),
            'ambient_dimension':n,'orbits':len(orbits),'steps':steps,'constraints':constraints,
            'seconds':time.monotonic()-start}

def audit_witnesses(data,certificate):
    results=[]
    for rec in data.get('results',[]):
        if not rec.get('exact_feasible'):continue
        counts=[0]*len(data['orbits'])
        for item in rec['support']:counts[item['orbit']]+=item['count']*item['multiplicity_unit']
        bad=[]
        for i,c in enumerate(certificate['constraints']):
            residue=(c['constant']+sum(a*b for a,b in zip(c['coefficients'],counts)))%c['modulus']
            if residue:bad.append({'constraint':i,'residue':residue,'modulus':c['modulus']})
        results.append({'case':rec.get('case'),'violations':bad})
    return results

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('fixture');ap.add_argument('--max-rounds',type=int,default=40)
    args=ap.parse_args();path=Path(args.fixture);data=json.loads(path.read_text())
    result=generate(data,args.max_rounds);result['witness_audits']=audit_witnesses(data,result)
    result['fixture_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    target=HERE/('all_word_'+path.stem+'.json');target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'constraints':len(result['constraints']),
                      'witness_audits':result['witness_audits'],'seconds':result['seconds'],'output':str(target)}),flush=True)

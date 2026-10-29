"""Exploratory necessary-condition solver, NEVER a categorical-model certificate.

Uses exact integer cyclotomic coordinates in Q(zeta_1600).  All displayed
positive witnesses are independently checked with integer arithmetic.
Full Galois orbits of (restriction, twist) are used, plus the induction Gram
matrix and Ng--Schauenburg indicator identities for n=1,2,3.
"""
from collections import defaultdict
from itertools import product
from math import gcd
from pathlib import Path
import json
import numpy as np
from scipy.sparse import csc_array
from scipy.optimize import milp, Bounds, LinearConstraint

HERE=Path(__file__).resolve().parent
N=1600
GENERATORS=(1151,901,577)  # CRT generators: (-1,1),(5,1),(1,2) mod(64,25)

def action(state,a):
    j,v,t=state
    r=a%5; ri=pow(r,-1,5)
    w=tuple(v[(ri*i)%5] for i in range(5))
    jj=(r*j)%5 if j>=0 else -1
    if j>=0 and r in (2,3):
        w=tuple(1-int(i==jj)-w[i] for i in range(5))
    return jj,w,(a*a*t)%N

def orbit(state):
    seen={state}; pending=[state]
    while pending:
        s=pending.pop()
        for a in GENERATORS:
            q=action(s,a)
            if q not in seen: seen.add(q);pending.append(q)
    return tuple(sorted(seen))

def power(t):
    """z^t modulo Phi_1600=z^640-z^480+z^320-z^160+1."""
    t%=N
    sign=1
    if t>=800:t-=800;sign=-1
    if t<640:return {t:sign}
    return {t-160:sign,t-320:-sign,t-480:sign,t-640:-sign}

def scalar_twist(a,b,t):
    # (a+b*d)*z^t with d=3+2z^320+2z^1280.
    out=defaultdict(int)
    for shift,m in [(0,a+3*b),(320,2*b),(1280,2*b)]:
        for k,c in power(t+shift).items():out[k]+=m*c
    return {k:c for k,c in out.items() if c}

fixed=[(0,(0,0,0,0,0),0),(0,(0,1,1,1,1),0)]
for i in range(1,5):
    fixed.append((0,tuple(int(k==i) for k in range(5)),0))
    fixed.append((0,tuple(int(k!=0 and k!=i) for k in range(5)),0))

mixed=[]
for bits in product(range(2),repeat=4):
    v=list(bits);v.insert(1,0)
    for q in range(5):mixed.append(orbit((1,tuple(v),320*q)))

seen=set(); pure=[]
for b in (1,2,5,10):
    for v in product(range(4),repeat=5):
        if sum(v)!=b:continue
        for t in range(N):
            s=(-1,v,t)
            if s in seen:continue
            o=orbit(s);seen.update(o)
            if any(sum(w[1][i]**2 for w in o)>10 for i in range(5)):continue
            pure.append(o)

print('candidate orbits:',len(mixed),'mixed',len(pure),'pure',flush=True)
orbits=mixed+pure
rhs={}
# Gram matrix minus fixed I(1) columns.
for i in range(5):
    for j in range(i,5):
        rhs[('gram',i,j)]=15+15*(i==j)-sum(s[1][i]*s[1][j] for s in fixed)
# Two simples, total b=4, in every twist eigenspace of I(g).
for q in range(5):
    rhs[('phase_count',q)]=2
    rhs[('phase_b',q)]=4
for i in (0,2,3,4):rhs[('incidence',i)]=5

def indicator_column(states):
    out=defaultdict(int)
    for j,v,t in states:
        a=int(j>=0);b=sum(v)
        for n in (1,2,3):
            coeffs=scalar_twist(a,b,n*t)
            for i,m in enumerate(v):
                if m:
                    for k,c in coeffs.items():out[('indicator',n,i,k)]+=m*c
    return {k:c for k,c in out.items() if c}

fixedind=indicator_column(fixed)
for key,c in fixedind.items():rhs[key]=-c
D=scalar_twist(10,20,0)
for i in range(1,5):
    for k,c in D.items():rhs[('indicator',3,i,k)]=rhs.get(('indicator',3,i,k),0)+c
# nu_2(x)=2e-1, e in {0,1}.  Others have nu_2=0.
for k,c in D.items():rhs[('indicator',2,0,k)]=rhs.get(('indicator',2,0,k),0)-c

columns=[]
for o in orbits:
    col=defaultdict(int,indicator_column(o))
    for j,v,t in o:
        for i in range(5):
            for k in range(i,5):col[('gram',i,k)]+=v[i]*v[k]
        if j==1:
            col[('phase_count',t//320)]+=1
            col[('phase_b',t//320)]+=sum(v)
            for i in (0,2,3,4):col[('incidence',i)]+=v[i]
    columns.append({k:c for k,c in col.items() if c})
columns.append({('indicator',2,0,k):-2*c for k,c in D.items()})

keys=sorted(set(rhs).union(*(c.keys() for c in columns)),key=str)
ki={k:i for i,k in enumerate(keys)}
rr=[];cc=[];dd=[]
for j,col in enumerate(columns):
    for k,c in col.items():rr.append(ki[k]);cc.append(j);dd.append(c)
A=csc_array((np.array(dd,dtype=float),(np.array(rr,dtype=np.int32),np.array(cc,dtype=np.int32))),shape=(len(keys),len(columns)))
y=np.array([rhs.get(k,0) for k in keys],dtype=float)
upper=np.full(len(columns),np.inf);upper[-1]=1
for j,o in enumerate(orbits):
    if any(state[0]>=0 and sum(state[1])==0 for state in o):upper[j]=0
print('matrix',A.shape,'nonzeros',len(dd),flush=True)
res=milp(np.zeros(len(columns)),integrality=np.ones(len(columns)),bounds=Bounds(0,upper),constraints=LinearConstraint(A,y,y),options={'time_limit':240,'mip_rel_gap':0})
print(res.message,flush=True)
if res.x is not None:
    x=np.rint(res.x).astype(int)
    exact=defaultdict(int)
    for col,m in zip(columns,x):
        for k,c in col.items():exact[k]+=int(m)*c
    assert all(exact.get(k,0)==rhs.get(k,0) for k in keys)
    out={'warning':'Exact necessary-condition witness only; NOT a modular datum or categorification.','nu2_x':int(2*x[-1]-1),'orbits':[{'multiplicity':int(m),'states':o} for m,o in zip(x,orbits) if m]}
    (HERE/'twist_gram_no_central_witness.json').write_text(json.dumps(out,indent=2)+'\n')
    print('exact integer witness saved, nu2',out['nu2_x'],'center rank',len(fixed)+sum(int(m)*len(o) for m,o in zip(x,orbits)),flush=True)
    print([(int(m),len(o),sum(o[0][1]),N//gcd(o[0][2],N)) for m,o in zip(x,pure and orbits) if m],flush=True)
else:
    (HERE/'twist_gram_no_central_status.json').write_text(json.dumps({'status':int(res.status),'message':res.message,'warning':'Floating solver infeasibility is not an exact proof.'},indent=2)+'\n')

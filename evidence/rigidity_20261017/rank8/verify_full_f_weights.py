"""Enumerate all full rank-four F slots and their proposed structural gauge weights.

This checks combinatorics and the torus implication only. It does not certify
that an arbitrary category admits the proposed simultaneously normalized charts.
"""
from itertools import product
import json
from pathlib import Path

# Objects (invertibility flag, g bit); 0=1,1=g,2=r,3=gr.
objs=[(0,0),(0,1),(1,0),(1,1)]
def basis(i,j,k):
    ni,bi=objs[i];nj,bj=objs[j];nk,bk=objs[k]
    if not ni or not nj:
        return [(0,0)] if (nk,bk)==(max(ni,nj),bi^bj) else []
    if not nk:
        return [(0,0)] if bk==bi^bj else []
    return [(1,0),(-1,0)] if bi^bj^bk==0 else [(0,1),(0,-1)]
weights=set(); counts={}; slots=0; block_sizes={}; reflection_checks=0
for a,b,c,d in product(range(4),repeat=4):
    left=[]; right=[]
    for p in range(4):
        for x,y in product(basis(a,b,p),basis(p,c,d)):
            left.append((p,x,y))
    for q in range(4):
        for z,t in product(basis(b,c,q),basis(a,q,d)):
            right.append((q,z,t))
    if len(left)!=len(right):raise ValueError('Associative block size')
    if left:block_sizes[str((a,b,c,d))]=len(left)
    for (_,x,y),(_,z,t) in product(left,right):
        wt=tuple(x[k]+y[k]-z[k]-t[k] for k in range(2))
        if wt[0]%2 or wt[1]%2 or sum(map(abs,wt))>4:
            raise ValueError(('Full F weight bound',wt,(a,b,c,d)))
        weights.add(wt);slots+=1;counts[str(wt)]=counts.get(str(wt),0)+1
        j_negative_count=sum(v==(0,-1) for v in (x,y,z,t))
        for exponent in (1,3,5,7):
            phase=(exponent*wt[0]+4*j_negative_count)%8
            if phase==0 and wt[0]!=0:
                raise ValueError(('Reflection-case nonzero H weight',wt,exponent,(x,y,z,t)))
            reflection_checks+=1
cases=[]
for a,b in product([1,3,5,7],repeat=2):
    allowed=sorted(w for w in weights if (a*w[0]+b*w[1])%8==0)
    epsilon=1 if (a-b)%4==0 else -1
    if not all(w[0]+epsilon*w[1]==0 for w in allowed):
        raise ValueError(('Torus annihilator',a,b,allowed))
    cases.append({'u_exponent_mod8':a,'v_exponent_mod8':b,'torus_slope':epsilon,'allowed_weights':allowed})
lattice_pairs=0
for a,b in product(weights,repeat=2):
    det=a[0]*b[1]-a[1]*b[0]
    if not det:continue
    for target in ((4,0),(0,4)):
        # Cramer's rule gives integral coefficients in the pair lattice.
        numerator_a=target[0]*b[1]-target[1]*b[0]
        numerator_b=a[0]*target[1]-a[1]*target[0]
        if numerator_a%det or numerator_b%det:
            raise ValueError(('Fourth-axis lattice containment',a,b,target))
    lattice_pairs+=1
report={'status':'PASS','categorical_normalization_certified':False,'classification_decisions':0,'independent_weight_pairs_checked':lattice_pairs,'J_reflection_phase_checks':reflection_checks,'nonempty_F_blocks':len(block_sizes),'full_F_coefficient_slots':slots,'weight_set':sorted(weights),'weight_counts':counts,'root_cases':cases,'scope':'All F-slot parity and weight bounds, and finite torus-annihilator implication; categorical structural normalization remains an independent premise.'}
print(json.dumps(report,indent=2))


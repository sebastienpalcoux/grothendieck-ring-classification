#!/usr/bin/env python3
"""Source-bound exact integral rank-eight proofs and independent models.

No Python assert is used. The same certificate is checked under python -O.
The census is loaded afresh, ordered independently, and all tensor entries
are compared with each model. Category existence is documented in PROOFS.md.
"""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'supplements/rank8/data/rank8_tables.txt.gz').exists())
sys.path.insert(0, str(ROOT / 'evidence/upper_residual_20261002b_recovery'))
from verify_recovery import read_source, validate_ring, adjoint_closure, fingerprint, require

EXCLUSIONS = {
 'R8_2_41': [1,1,1,1,2,2,2,4],
 'R8_2_86': [1,1,1,1,2,2,2,4],
 'R8_2_162': [1,1,1,1,2,2,2,4],
 'R8_2_140': [1,1,1,1,2,4,4,4],
 'R8_2_694': [1,1,1,1,2,4,4,4],
 'R8_2_697': [1,1,1,1,4,4,4,4],
 'R8_2_808': [1,1,2,6,6,6,6,6],
}

def dimension_vector(T, multiset):
    for ds in sorted(set(itertools.permutations(multiset[1:]))):
        d = (1,) + ds
        if all(sum(c*d[k] for k,c in enumerate(T[i][j])) == d[i]*d[j]
               for i,j in itertools.product(range(8), repeat=2)):
            return list(d)
    raise ValueError('no positive exact dimension character')

def order(T, g):
    x = 0
    for a in range(1,9):
        hits = [k for k,c in enumerate(T[x][g]) if c]
        require(len(hits)==1 and T[x][g][hits[0]]==1, 'invertible multiplication')
        x = hits[0]
        if x == 0: return a
    raise ValueError('invertible order')

def check_exclusion(ID,T):
    du = validate_ring(T)
    d = dimension_vector(T,EXCLUSIONS[ID])
    inv = [i for i,v in enumerate(d) if v==1]
    rec = {'dimensions':d, 'global_dimension':sum(v*v for v in d),
           'invertibles':inv, 'invertible_orders':[order(T,g) for g in inv],
           'dual':du, 'adjoint_indices':adjoint_closure(T,du)}
    if ID in ('R8_2_41','R8_2_86','R8_2_162'):
        odd = [i for i,v in enumerate(d) if v==4]
        require(len(odd)==1,'unique odd object')
        m = odd[0]; neutral = [i for i in range(8) if i!=m]
        require(sum(d[i]**2 for i in neutral)==16,'neutral dimension16')
        for i,j in itertools.product(neutral,repeat=2):
            require(T[i][j][m]==0,'neutral closure')
        for i in neutral:
            require(T[i][m]==T[m][i]==[d[i]*int(k==m) for k in range(8)],'rank-one bimodule')
        require(all(T[m][m][k]==(d[k] if k in neutral else 0) for k in range(8)), 'odd square regular')
        if ID!='R8_2_162':
            require(4 in rec['invertible_orders'],'C4 excludes selfdual Hopf16')
        else:
            require(any(du[i]!=i for i in neutral if d[i]==2),'non-selfdual excludes RepD16')
        rec.update(neutral_indices=neutral,rank_one_component=m,neutral_dual_rank_required=7)
    elif ID=='R8_2_140':
        neutral = [0,1,2,3,7]; gi = [0,1,2,7]; e = 3
        require(set(gi)==set(inv) and d[e]==2,'TY neutral labels')
        require(4 in rec['invertible_orders'],'TY groupC4')
        require(T[e][e]==[int(k in gi) for k in range(8)],'TY square')
        for i,j in itertools.product(neutral,repeat=2):
            require(all(not T[i][j][k] for k in (4,5,6)),'neutral closure')
        for m in (4,5,6):
            for i in neutral:
                require(T[i][m]==T[m][i]==[d[i]*int(k==m) for k in range(8)],'rank-one neutral module')
        rec.update(neutral_indices=neutral,neutral_dimension=8,rank_one_modules=[4,5,6])
    else:
        require(rec['adjoint_indices']==list(range(8)),'whole adjoint')
        require(all(T[g][i]==[int(k==i) for k in range(8)] for g in inv for i in range(8) if d[i]>1), 'invertibles fix nonunits')
        if ID=='R8_2_697':
            require(rec['invertible_orders']==[1,2,2,2],'V4 invertibles')
            rec['forced_first_descent_type']={'dimension':34,'type':[[1,2],[2,8]]}
            rec['forced_combined_group']='V4'
        elif ID=='R8_2_808':
            rec['forced_first_descent_type']={'dimension':93,'type':[[1,3],[3,10]]}
            rec['forced_combined_group']='S3'
        else:
            rec['forced_first_descent_dimension']=28
            rec['nonpointed_dimension28_adjoint_type']=[[1,2],[2,3]]
    return rec

def pointed_equivariantization(elements, add, act, m):
    zero=elements[0]
    remaining=set(elements); orbits=[]
    while remaining:
        a=min(remaining); orb=[]; b=a
        for _ in range(m): orb.append(b); b=act(b)
        orb=sorted(set(orb)); require(b==a,'action order')
        require(len(orb)==1 if a==zero else len(orb)==m,'free action outside zero')
        remaining.difference_update(orb)
        if a!=zero:orbits.append(orb)
    orbits.sort(key=lambda O:O[0])
    n=m+len(orbits);T=[[[0]*n for _ in range(n)] for _ in range(n)]
    orbit_index={a:m+i for i,O in enumerate(orbits) for a in O}
    for i,j in itertools.product(range(n),repeat=2):
        if i<m and j<m:T[i][j][(i+j)%m]=1
        elif i<m:T[i][j][j]=1
        elif j<m:T[i][j][i]=1
        else:
            counts=collections.Counter(add(a,b) for a in orbits[i-m] for b in orbits[j-m])
            require(counts[zero]%m==0,'zero-pair regular stabilizer multiplicity')
            for k in range(m):T[i][j][k]=counts[zero]//m
            for O in orbits:
                require(len({counts[a] for a in O})==1,'equivariant orbit coefficient')
                T[i][j][orbit_index[O[0]]]=counts[O[0]]
    return T,orbits

def pointed_models():
    c4=list(itertools.product(range(4),repeat=2))
    c2=list(itertools.product(range(2),repeat=4))
    out={}
    out['R8_2_244']=pointed_equivariantization(c4,lambda a,b:tuple((x+y)%4 for x,y in zip(a,b)),lambda a:((-a[1])%4,(a[0]-a[1])%4),3)
    out['R8_2_289']=pointed_equivariantization(c2,lambda a,b:tuple(x^y for x,y in zip(a,b)),lambda a:(a[1],a[0]^a[1],a[3],a[2]^a[3]),3)
    out['R8_2_143']=pointed_equivariantization(list(range(17)),lambda a,b:(a+b)%17,lambda a:4*a%17,4)
    out['R8_2_179']=pointed_equivariantization(c2,lambda a,b:tuple(x^y for x,y in zip(a,b)),lambda a:(a[3],a[0]^a[3],a[1]^a[3],a[2]^a[3]),5)
    return out

# A compact exact Q(zeta21) implementation; integers only.
# Phi21=x^12-x^11+x^9-x^8+x^6-x^4+x^3-x+1.
PHI=[1,-1,0,1,-1,0,1,0,-1,1,0,-1,1]
ZERO=(0,)*12
ONE=(1,)+(0,)*11
def reduce_poly(v):
    v=list(v)+[0]*max(0,12-len(v))
    for a in range(len(v)-1,11,-1):
        if v[a]:
            c=v[a]
            for k in range(12):v[a-12+k]-=c*PHI[k]
    return tuple(v[:12])
ROOTS=[reduce_poly([0]*a+[1]) for a in range(21)]
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def times(a,b):
    out=[0]*23
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:out[i+j]+=x*y
    return reduce_poly(out)
def scale(a,v):return tuple(v*x for x in a)
def conjugate(a):
    out=ZERO
    for i,v in enumerate(a):out=plus(out,scale(ROOTS[-i%21],v))
    return out

def f8mul(a,b):
    ans=0
    while b:
        if b&1:ans^=a
        b>>=1;a<<=1
        if a&8:a^=11
    return ans
def f8pow(a,n):
    ans=1
    for _ in range(n):ans=f8mul(ans,a)
    return ans
def trace(a):return a^f8pow(a,2)^f8pow(a,4)

def agammal_model():
    require(ROOTS[0]==ONE and reduce_poly([0]*21+[1])==ONE,'cyclotomic period')
    els=list(itertools.product(range(8),range(1,8),range(3)))
    def product(g,h):
        v,a,t=g;w,b,u=h
        return (v^f8mul(a,f8pow(w,2**t)),f8mul(a,f8pow(b,2**t)),(t+u)%3)
    generators=[(1,1,0),(0,2,0),(0,1,1)]
    generated={(0,1,0)}
    while True:
        nxt=generated|{product(g,h) for g in generated for h in generators}
        if nxt==generated:break
        generated=nxt
    require(len(generated)==168,'affine semilinear generators')
    for g,h,k in itertools.product(generators,repeat=3):
        require(product(product(g,h),k)==product(g,product(h,k)),'generator associativity')
    logs={f8pow(2,e):e for e in range(7)}
    require(len(logs)==7 and all(trace(a) in (0,1) for a in range(8)),'F8 exact arithmetic')
    chars=[[] for _ in range(8)]
    for v,a,t in els:
        for s in range(3):chars[s].append(ROOTS[7*s*t%21])
        for j,O in enumerate(((1,2,4),(3,5,6)),3):
            z=ZERO
            if t==0:
                for e in O:z=plus(z,ROOTS[3*e*logs[a]%21])
            chars[j].append(z)
        z=sum(((-1)**trace(f8mul(v,f8pow(r,6))) for r in range(1,8)
               if f8mul(a,f8pow(r,2**t-1))==1),0)
        for s in range(3):chars[5+s].append(scale(ROOTS[7*s*t%21],z))
    cc=[[conjugate(v) for v in row] for row in chars]
    def integer(q,den):
        require(all(not c for c in q[1:]) and q[0]%den==0,'exact integral character inner product')
        return q[0]//den
    for i,j in itertools.product(range(8),repeat=2):
        value=ZERO
        for a,b in zip(chars[i],cc[j]):value=plus(value,times(a,b))
        require(integer(value,168)==int(i==j),'character orthogonality')
    dims=[1,1,1,3,3,7,7,7]
    require(sum(d*d for d in dims)==168,'complete character degrees')
    T=[[[0]*8 for _ in range(8)] for _ in range(8)]
    for i,j in itertools.product(range(8),repeat=2):
        prod=[times(a,b) for a,b in zip(chars[i],chars[j])]
        for k in range(8):
            value=ZERO
            for a,b in zip(prod,cc[k]):value=plus(value,times(a,b))
            T[i][j][k]=integer(value,168)
    return T,{'group_order':168,'character_dimensions':dims,'field_polynomial':PHI,'orthogonality_pairs':64,'fusion_coefficients':512}

def compare_model(T,p,source):
    require(sorted(p)==list(range(8)),'model basis bijection')
    validate_ring(T)
    for i,j,k in itertools.product(range(8),repeat=3):
        require(T[i][j][k]==source[p[i]][p[j]][p[k]],'independent model coefficient mismatch')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repository',type=Path,default=ROOT);ap.add_argument('--output',type=Path);args=ap.parse_args()
    started=time.monotonic();source=read_source(args.repository,8)
    decisions={d['id']:d for d in json.loads((args.repository/'evidence/upper_residual_20261002b_recovery/decisions.json').read_text())}
    result={'status':'PASS','python_optimized':not __debug__,'general_exclusions':{},'unitary_models':{}}
    for ID in EXCLUSIONS:
        require(fingerprint(source[ID])==decisions[ID]['census_tensor_sha256'],'source hash')
        result['general_exclusions'][ID]=check_exclusion(ID,source[ID])
    for ID,(T,orbits) in pointed_models().items():
        compare_model(T,decisions[ID]['model_to_census'],source[ID])
        result['unitary_models'][ID]={'model_to_census':decisions[ID]['model_to_census'],'orbits':orbits,'model_tensor_sha256':fingerprint(T),'coefficients_compared':512}
    T,rec=agammal_model();ID='R8_2_237';compare_model(T,decisions[ID]['model_to_census'],source[ID]);rec['model_to_census']=decisions[ID]['model_to_census'];rec['model_tensor_sha256']=fingerprint(T);result['unitary_models'][ID]=rec
    result['seconds']=round(time.monotonic()-started,3)
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()

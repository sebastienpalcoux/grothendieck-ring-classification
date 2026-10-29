#!/usr/bin/env python3
"""Finite exact R928 phase restrictions; no optimizer and no category claim.
Rebuilds all phase allocations from source-bound dimensions and N_W.
The categorical premises are stated in REPORT.md.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from itertools import combinations_with_replacement
import hashlib,json,math,sys
HERE=Path(__file__).resolve().parent
N=288
DEG=96
# Phi_288(x)=x^96-x^48+1; sparse integer coordinates in its power basis.
def root(k):
    k%=N; d={k:1}
    for i in range(k,DEG-1,-1):
        a=d.pop(i,0)
        if a:
            d[i-DEG//2]=d.get(i-DEG//2,0)+a
            d[i-DEG]=d.get(i-DEG,0)-a
    return tuple(sorted((i,a) for i,a in d.items() if a))
def add(*vs):
    d=Counter()
    for v in vs:
        for i,a in v:d[i]+=a
    return tuple(sorted((i,a) for i,a in d.items() if a))
def scale(k,v):return tuple((i,k*a) for i,a in v if k*a)
def mul(a,b):return add(*(scale(x*y,root(i+j)) for i,x in a for j,y in b))
RT=[root(i) for i in range(N)]
ONE=RT[0]
sqrt2=add(RT[N//8],RT[-N//8]);sqrt3=add(RT[N//12],RT[-N//12]);sqrt6=mul(sqrt2,sqrt3)
xi=RT[N//8]
def encode_dimension(d):return add(*(scale(int(a),b) for a,b in zip(d,(ONE,sqrt2,sqrt3,sqrt6))))
def need(b,msg):
    if not b:raise ValueError(msg)
source=HERE/'prior/spectral_reduction.json'
p=next(p for p in json.loads(source.read_text())['patterns'] if p['pattern']==186)
W=p['N_W']; dims=list(map(encode_dimension,p['dimensions']));n=len(W)
need(n==20,'pattern186 rank')
D=encode_dimension([144,96,80,56]);D2=mul(D,D)
need(add(*(scale(2,mul(d,d)) for d in dims))==D2,'global dimension')
# Unit-group square orbits; complete fibers have integral orbit masses.
units=[a for a in range(N) if math.gcd(a,N)==1]
sq=sorted(set(a*a%N for a in units));orbits=[];left=set(range(N))
while left:
    k=min(left);o=sorted(set(k*a%N for a in sq));left.difference_update(o);orbits.append(o)
# This common conductor includes every allowed order<=five-orbit bound.
small=[o for o in orbits if len(o)<=5]
need(all(not add(*(RT[k] for k in o)) for o in small if len(o)>1),'nonsingleton orbit sums')
# Four exact three-B sums. A superset of individual roots is used here,
# so no missing orbit allocation could accidentally be excluded.
allowedB=[k for k in range(N) if (48*k)%N==0 or (72*k)%N==0]
pairs={}
for a,b in combinations_with_replacement(allowedB,2):pairs.setdefault(add(RT[a],RT[b]),[]).append((a,b))
Bcases={}
for t in range(0,N,N//24):
    target=scale(-1,add(ONE,scale(2,RT[t]),mul(sqrt6,xi)))
    found=set()
    for a in allowedB:
        for b,c in pairs.get(add(target,scale(-1,RT[a])),[]):found.add(tuple(sorted((a,b,c))))
    if found:Bcases[t]=sorted(found)
need(sum(map(len,Bcases.values()))==4,'four three-B phase cases')
# Enumerate multisets of complete square orbits of total mass5.
# Target associates t and the unique K phase; no pretabulated allocation.
targets={}
for t in Bcases:
    target=scale(-1,add(ONE,scale(2,RT[t]),scale(2,mul(sqrt3,xi))))
    for k in range(0,N,N//24):targets.setdefault(add(target,scale(-4,RT[k])),[]).append((t,k))
AK=[];H=[];nodes=0
os=small;sums=[add(*(RT[k] for k in o)) for o in os]
def visit(start,mass,z,chosen,mode):
    global nodes
    nodes+=1
    if mass==0:
        flat=sorted(k for i in chosen for k in os[i])
        if mode=='AK':
            for t,k in targets.get(z,[]):AK.append((t,k,flat))
        elif not z:H.append(flat)
        return
    for j in range(start,len(os)):
        if len(os[j])<=mass:visit(j,mass-len(os[j]),add(z,sums[j]),chosen+[j],mode)
visit(0,5,(),[],'AK');visit(0,4,(),[],'H')
need(len(AK)==10 and len(H)==312,'finite A/K and H domains')
# AMV determinant identity with three W arguments.
M=[sum(W[4][r]*W[r][j] for r in range(n)) for j in range(n)]
V=[]
for t,k,A in AK:
    for B in Bcases[t]:
        for h in H:
            phase=[0]*4+[N//4,t]+A+list(B)+h+[k,t]
            need(len(phase)==n,'phase indexing')
            residues=[(M[j]*(3*phase[4]+phase[j])-sum(3*W[4][r]*W[r][j]*phase[r] for r in range(n)))%N for j in range(n)]
            if not any(residues):V.append({'t':t,'K':k,'A':A,'B':B,'H':h,'phase':phase})
need(len(V)==48,'48 AMV survivors')
# Modular indicator numerators. The factor2 changes divisor dim(B)=D²/2
# to D². Every product is exact integer cyclotomic arithmetic.
DD=[[mul(dims[i],dims[j]) for j in range(n)] for i in range(n)]
def indicator_numerator(phase,m):
    return add(*(scale(2*W[i][j],mul(DD[i][j],RT[(m*(phase[i]-phase[j]))%N])) for i in range(n) for j in range(n) if W[i][j]))
def rational_ratio(z,den):
    dd=dict(den);zz=dict(z);i=next(iter(dd));q=Fraction(zz.get(i,0),dd[i])
    return q if scale(q,den)==z else None
V2=[r for r in V if indicator_numerator(r['phase'],2)==D2]
need(len(V2)==12,'12 positive-second-indicator survivors')
V4=[];rejected=[]
for r in V2:
    z=indicator_numerator(r['phase'],4)
    # N_W is symmetric, so the indicator expression is real.
    need(all(W[i][j]==W[j][i] for i in range(n) for j in range(n)),'real indicator')
    q=rational_ratio(z,D2)
    if q is not None and q.denominator==1:
        V4.append(dict(r,nu4=int(q)))
    else:rejected.append(dict(r,nu4_numerator=z))
need(len(V4)==2 and sorted(r['nu4'] for r in V4)==[2,40],'two fourth-indicator survivors')
out={'status':'PASS','scope':'two R928 patterns excluded; pattern186 phase domain restricted, not a categorification decision',
     'conductor':N,'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
     'B_cases':Bcases,'AK_cases':AK,'H_count':len(H),'enumeration_nodes':nodes,'AMV_count':len(V),'nu2_count':len(V2),
     'nu4_rejected_count':len(rejected),'remaining':V4}
# Compatibility receipt for the separately audited matching/pattern40 replay.
legacy={'H_quartets':[[6*x for x in h] for h in H],
        'survivors':[[r['t']//2,6*r['K'],[6*x for x in r['A']],
                      [x//2 for x in r['B']],[6*x for x in r['H']]] for r in V]}
(HERE/'vafa_probe.json').write_text(json.dumps(legacy,indent=2)+'\n')
(HERE/'phase_reduction_verification.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: B4; AK10; H312; AMV48; nu2 12; nu4 2. R928 remains unresolved.')

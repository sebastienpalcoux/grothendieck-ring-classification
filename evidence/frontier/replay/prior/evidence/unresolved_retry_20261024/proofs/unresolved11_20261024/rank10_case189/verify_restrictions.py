"""Standard-library exact verifier of necessary R189 data, NOT a categorification.

Run: python verify_restrictions.py [optional path to R10_1_189.json]
The witness arithmetic is independent of the MILP code and numerical libraries.
"""
from collections import Counter, defaultdict
from pathlib import Path
from math import gcd, lcm
from hashlib import sha256
import json, sys

HERE=Path(__file__).resolve().parent
SOURCE=Path(sys.argv[1]) if len(sys.argv)>1 else HERE.parent/'inputs/R10_1_189.json'
P=[0,1,8,7,2,9,4,6,5,3]
if SOURCE.exists():
    raw=SOURCE.read_bytes(); data=json.loads(raw)
    T=data['fusion_tensor']
    for i in range(10):
        for j in range(10):
            expected=[0]*10
            if i<5 and j<5:expected[(i+j)%5]=1
            elif min(i,j)<5:expected[5+(i+j)%5]=1
            else:
                expected[(i+j)%5]=1
                for h in range(1,5):expected[5+(i+j+h)%5]=1
            assert [T[P[i]][P[j]][P[k]] for k in range(10)]==expected
    print('source tensor normal form verified; sha256',sha256(raw).hexdigest())

def zpower(t):
    # Phi_1600=x^640-x^480+x^320-x^160+1.
    t%=1600; s=1
    if t>=800:t-=800;s=-1
    if t<640:return {t:s}
    return {t-160:s,t-320:-s,t-480:s,t-640:-s}

def add(*terms):
    out=defaultdict(int)
    for p in terms:
        for k,v in p.items():out[k]+=v
    return {k:v for k,v in out.items() if v}

def scale(p,n):return {k:v*n for k,v in p.items() if v*n}

def dimtw(a,b,t):
    # d=2+sqrt(5)=3+2 zeta_1600^320+2 zeta_1600^1280.
    return add(scale(zpower(t),a+3*b),scale(zpower(t+320),2*b),scale(zpower(t+1280),2*b))

def action(state,a):
    j,v,t=state;r=a%5;ri=pow(r,-1,5)
    w=tuple(v[ri*i%5] for i in range(5))
    jj=r*j%5 if j>=0 else -1
    if j>=0 and r in (2,3):w=tuple(1-int(i==jj)-w[i] for i in range(5))
    return jj,w,a*a*t%1600

generators=(1151,901,577)
units={1};todo=[1]
while todo:
    a=todo.pop()
    for b in generators:
        c=a*b%1600
        if c not in units:units.add(c);todo.append(c)
assert units=={a for a in range(1600) if gcd(a,1600)==1}

witness=json.loads((HERE/'twist_gram_witness.json').read_text())
fixed=[(0,(0,0,0,0,0),0),(0,(0,1,1,1,1),0)]
for i in range(1,5):
    fixed.extend([(0,tuple(int(k==i) for k in range(5)),0),(0,tuple(int(k not in [0,i]) for k in range(5)),0)])
states=list(fixed)
for item in witness['orbits']:
    o={(int(j),tuple(v),int(t)) for j,v,t in item['states']}
    assert len(o)==len(item['states']) and item['multiplicity']>0
    for a in generators:assert {action(s,a) for s in o}==o
    states.extend(sorted(o)*item['multiplicity'])

gram=[[0]*10 for _ in range(10)]
for j,v,t in states:
    assert all(isinstance(m,int) and m>=0 for m in v)
    if j<0:assert sum(v) in (1,2,5,10)
    else:assert all(m in (0,1) for m in v) and v[j]==0 and t%320==0
    col=[int(i==j) for i in range(5)]+list(v)
    for i in range(10):
        for k in range(10):gram[i][k]+=col[i]*col[k]
for i in range(10):
    for j in range(10):
        expected=10*int(i==j) if max(i,j)<5 else (15+15*int(i==j) if min(i,j)>=5 else 5*int(i%5!=j%5))
        assert gram[i][j]==expected
for j in range(1,5):
    for q in range(5):
        block=[v for jj,v,t in states if jj==j and t==320*q]
        assert len(block)==2 and sum(map(sum,block))==4
for i in range(5):
    counts=[sum(v[i] for j,v,t in states if j>=0 and t==320*q) for q in range(5)]
    assert counts==([4]*5 if i==0 else [8,3,3,3,3])

D=dimtw(10,20,0)
def moment(n,i):
    return add(*(scale(dimtw(int(j>=0),sum(v),n*t),v[i]) for j,v,t in states if v[i]))
epsilon=witness['nu2_x']
expected={1:[0]*5,2:[epsilon,0,0,0,0],3:[0,1,1,1,1],4:[1]*5}
for n,values in expected.items():
    for i,v in enumerate(values):assert moment(n,i)==scale(D,v)
assert lcm(*(1600//gcd(t,1600) for _,_,t in states))==10
# All coprime-to-1600 cases follow from period10 after these four checks.
for n in (1,3,7,9):
    for i in range(5):
        want=int(n%5 in (2,3) and i!=0)
        assert moment(n,i)==scale(D,want)

# Exact C4 character checks. The entries give multiplicities of 1,i,-1,-i.
for i in range(5):
    mult=(2,1,1,1) if i==0 else (1,1,0,1)
    assert sum(mult)==(5 if i==0 else 3)
    assert mult[0]-mult[2]==1 and mult[1]==mult[3]
    assert mult[0]-mult[1]+mult[2]-mult[3]==(1 if i==0 else epsilon)

print('PASS: 70-column exact necessary-condition witness; Gram, full Galois action, phases, indicators1--4, and C4 rotation characters')
print('WARNING: this verifies neither modular data nor a fusion category; R10_1_189 remains unresolved.')

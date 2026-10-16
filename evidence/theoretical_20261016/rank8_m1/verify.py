#!/usr/bin/env python3
"""Exact source and arithmetic checks for the no-central-lift proof.

This does not verify category theory, central-lift existence, or a new
rank-eight exclusion. It checks every finite algebraic assertion used here.
"""
from pathlib import Path
import hashlib,itertools,json,sys
import sympy as s

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def require(ok,message):
    if not ok:raise ValueError(message)
def load(path):return json.loads(path.read_text())
def td(t):return hashlib.sha256(json.dumps(t,separators=(',',':')).encode()).hexdigest()
def fusion_check(n):
    k=len(n)
    require(all(n[0][a][b]==int(a==b) and n[a][0][b]==int(a==b)
                for a,b in itertools.product(range(k),repeat=2)), 'unit')
    require(all(sum(n[a][b][z]*n[z][c][v]for z in range(k))==
                sum(n[b][c][z]*n[a][z][v]for z in range(k))
                for a,b,c,v in itertools.product(range(k),repeat=4)), 'associativity')
def dual(n):return [next(j for j in range(len(n)) if n[i][j][0])for i in range(len(n))]

tensors=load(HERE/'source_tensors.json')
ledger={x['id']:x for x in load(ROOT/'supplements/rank8/data/decisions.json')}
profiles={}
for rid,n in tensors.items():
    require(td(n)==ledger[rid]['tensor_sha256'], 'source tensor hash '+rid)
    require(ledger[rid]['status']=='unresolved', 'unexpected ledger transition '+rid)
    fusion_check(n);du=dual(n)
    group=[i for i in range(8)if sum(n[i][du[i]])==1]
    noninv=[i for i in range(8)if i not in group]
    require(len(group)==len(noninv)==4,'four+four profile')
    r=next((i for i in noninv if du[i]==i),noninv[0])
    phi={g:next(h for h in group if n[r][g]==n[h][r])for g in group}
    require(all(sum(n[a][b][k]for k in group)==1 and
                all(n[a][b][k]==1 for k in noninv)
                for a,b in itertools.product(noninv,repeat=2)),'uniform quadratic rules')
    require(len({next(k for k,v in enumerate(n[g][r])if v)for g in group})==4,'free group action')
    profiles[rid]={'invertibles':group,'noninvertibles':noninv,'duality':du,
                   'rho':r,'phi':phi,'tensor_sha256':td(n),'status':'unresolved'}

# Independent orbit construction from Q1 and Ising.
q=[[[0]*4 for _ in range(4)]for _ in range(4)]
for a,b in itertools.product(range(4),repeat=2):
    g=(a%2)^(b%2);e=a//2+b//2
    if e<2:q[a][b][g+2*e]=1
    else:q[a][b][g]=1;q[a][b][2]=q[a][b][3]=2
i=[[[0]*3 for _ in range(3)]for _ in range(3)]
for a,b in itertools.product(range(3),repeat=2):
    if not a:i[a][b][b]=1
    elif not b:i[a][b][a]=1
    elif a==b==1:i[a][b][0]=1
    elif a==b==2:i[a][b][0]=i[a][b][1]=1
    else:i[a][b][2]=1
act=lambda x:(x[0]^1,1-x[1]if x[1]<2 else 2)
reps=[];orbit={}
for x in itertools.product(range(4),range(3)):
    if x not in orbit:
        orbit[x]=orbit[act(x)]=len(reps);reps.append(x)
n=[[[0]*6 for _ in range(6)]for _ in range(6)]
for a,b in itertools.product(range(6),repeat=2):
    x,y=reps[a],reps[b]
    for u,v in itertools.product(range(4),range(3)):
        n[a][b][orbit[u,v]]+=q[x[0]][y[0]][u]*i[x[1]][y[1]][v]
fusion_check(q);fusion_check(n)
source=load(HERE/'rank6_source.json')
census={x['id']:x for x in load(ROOT/'supplements/rank6/data/census.json')}
require(source==census['R6_4_373'],'rank-six source snapshot')
p=[0,1,4,3,2,5]
require(all(source['N'][a][b][c]==n[p[a]][p[b]][p[c]]
            for a,b,c in itertools.product(range(6),repeat=3)),'216 tensor coefficients')
decision=next(x for x in load(ROOT/'supplements/rank6/data/decisions.json')if x['id']=='R6_4_373')
require(decision['status']=='excluded','retained rank-six status')

# Character/formal-codegree and induction arithmetic.
d=s.symbols('d');mod=d*d-4*d-1
red=lambda x:s.rem(s.expand(x),mod,d)
ds=[1,1,s.sqrt(2),d,d,s.sqrt(2)*d]
require(all(red(sum(n[a][b][c]*ds[c]for c in range(6))-ds[a]*ds[b])==0
            for a,b in itertools.product(range(6),repeat=2)),'FP dimensions')
# Irreducible characters are f=-1,u=0,r=+/-1, and
# f=1,u=+/-sqrt(2),r=2+/-sqrt(5).
characters=[]
for v in [1,-1]:characters.append([1,-1,0,v,-v,0])
for u,r in itertools.product([s.sqrt(2),-s.sqrt(2)],[2+s.sqrt(5),2-s.sqrt(5)]):
    characters.append([1,1,u,r,r,u*r])
for ch in characters:
    require(all(s.simplify(sum(n[a][b][c]*ch[c]for c in range(6))-ch[a]*ch[b])==0
                for a,b in itertools.product(range(6),repeat=2)),'character')
fcs=[s.simplify(sum(v*v for v in ch))for ch in characters]
require(sorted(map(str,fcs))==sorted(map(str,[4,4,40+16*s.sqrt(5),40+16*s.sqrt(5),40-16*s.sqrt(5),40-16*s.sqrt(5)])),'formal codegrees')
fi1=[sum(n[a][a][b]for a in range(6))for b in range(6)]
require(fi1==[6,2,0,8,8,0],'FI1 coefficients')
D=8+16*d;T=16+72*d;K=8+32*d
require(red(D*d-T)==0,'I(r) total dimension')
gap=s.expand(T*(T+D)-K*(3*T+D))
require(gap==-64-512*d-1088*d*d,'fermion moment gap')
require(red(gap)==-1152-4864*d,'strict negativity at d>0')
require(red(2*d*(4+8*d)-2*(8+24*d))==24*d,'semion remaining mass')

print(json.dumps({'status':'PASS','optimized':bool(sys.flags.optimize),
    'source_profiles':profiles,'conditional_rank6_ring':'R6_4_373',
    'all_216_coefficients_matched':True,'rank6_census_to_model':p,
    'fermion_moment_gap_reduced':str(red(gap)),
    'semion_real_trace_deficit':8,'new_rank8_decisions':0,
    'scope':'Exact finite checks supporting the no-central-lift theorem; the three rank-eight cases remain unresolved.'},indent=2))

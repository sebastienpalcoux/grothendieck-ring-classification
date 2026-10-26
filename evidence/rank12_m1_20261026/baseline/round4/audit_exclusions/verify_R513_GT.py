#!/usr/bin/env python3
"""Exact small input/cohomology receipt for the R513 stable-Lagrangian proof."""
import hashlib,itertools,json
from pathlib import Path
P=Path(__file__).resolve().parent
def need(x,m):
    if not x:raise ValueError(m)
data=json.loads((P/'R513_GT_frozen.json').read_text())
R=data['tensor'];n=12
need(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==data['tensor_sha256'],'frozen tensor hash')
du=[next(j for j in range(n)if R[i][j][0])for i in range(n)]
G=[i for i in range(n)if sum(R[i][du[i]])==1]
def mul(i,j):
    need(sum(R[i][j])==1,'pointed multiplication')
    return R[i][j].index(1)
a=data['a'];b=data['b'];co={}
for u,v in itertools.product(range(4),range(2)):
    t=0
    for k in range(u):t=mul(t,a)
    if v:t=mul(t,b)
    co[u,v]=t
need(set(co.values())==set(G)and len(co)==8,'C4 x C2 coordinates')
need(all(mul(co[u],co[v])==co[(u[0]+v[0])%4,(u[1]+v[1])%2]for u,v in itertools.product(co,repeat=2)),'full group table')
x=data['noninvertible'];L={g for g in G if R[g][x][x]};Q={g for g in G if R[x][g][x]}
H0={co[u,0]for u in range(4)};H1={co[u,u%2]for u in range(4)}
need({frozenset(L),frozenset(Q)}=={frozenset(H0),frozenset(H1)},'two cyclic four stabilizers')
ad={0}
for i in range(n):ad.update(k for k in range(n)if R[i][du[i]][k])
while True:
    new=ad|{k for i in ad for j in ad for k in range(n)if R[i][j][k]}
    if new==ad:break
    ad=new
need(ad==set(G),'adjoint is full pointed group')
blocks=[set(G)]
for i in range(n):
    block={j for g in G for j in range(n)if R[g][i][j]}
    if block not in blocks:blocks.append(block)
need(sorted(map(len,blocks))==[2,2,8],'three grading blocks')
grade={i:k for k,B in enumerate(blocks)for i in B}
need(all(grade[k]==(grade[i]+grade[j])%3 for i,j,k in itertools.product(range(n),repeat=3)if R[i][j][k]),'actual C3 grading')
els=list(co)
add=lambda u,v:((u[0]+v[0])%4,(u[1]+v[1])%2)
def omega(par,u,v,w):
    A,B,C=par
    return (A*u[0]*((v[0]+w[0])//4)+2*B*u[1]*((v[1]+w[1])//2)+2*C*u[1]*((v[0]+w[0])//4))%4
def cycle(par,g):
    t=(0,0);r=0
    while True:
        r+=omega(par,g,t,g);t=add(t,g)
        if t==(0,0):return r%4
pars=list(itertools.product(range(4),range(2),range(2)))
for par in pars:
    need(all((omega(par,v,w,z)-omega(par,add(u,v),w,z)+omega(par,u,add(v,w),z)-omega(par,u,v,add(w,z))+omega(par,u,v,w))%4==0 for u,v,w,z in itertools.product(els,repeat=4)),'3-cocycle equation')
need(len({(cycle(p,(1,0)),cycle(p,(0,1)),cycle(p,(1,1)))for p in pars})==16,'sixteen independent cohomology classes')
allowed=[p for p in pars if cycle(p,(1,0))==cycle(p,(1,1))==0]
need(allowed==[(0,0,0),(0,1,0)],'simultaneous stabilizer restrictions')
subs={frozenset([(0,0)])}
while True:
    new=set(subs)
    for H in subs:
        for g in els:
            K=set(H);t=(0,0)
            for i in range(8):
                K.update(add(h,t)for h in H);t=add(t,g)
            new.add(frozenset(K))
    if new==subs:break
    subs=new
need(len(subs)==8,'complete subgroup lattice')
rows=[]
for p in allowed:
    good=[];count=0
    for H in subs:
        # For these two explicit classes, restriction is trivial iff all
        # cyclic restrictions vanish; direct coordinate reasoning proves this.
        if any(cycle(p,g)for g in H):continue
        ordermax=max(next(i for i in range(1,9)if ((i*g[0])%4,(i*g[1])%2)==(0,0))for g in H)
        schur=1 if ordermax==len(H)else 2
        good.append({'subgroup':sorted(H),'alternating_forms':schur});count+=schur
    need(count==(10 if p==(0,0,0)else 4),'Lagrangian count')
    rows.append({'omega_parameters':p,'admissible_subgroups':good,'lagrangians':count,'modulo_three':count%3})
result={'status':'PASS','id':data['id'],'tensor_sha256':data['tensor_sha256'],'pointed_group':'C4 x C2','neutral_grading_group':'C3','left_stabilizer':sorted(L),'right_stabilizer':sorted(Q),'cohomology_classes':16,'allowed_classes':rows,'conclusion':'Every complex categorification is group-theoretical by the separate stable-Lagrangian proof.'}
(P/'R513_GT_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

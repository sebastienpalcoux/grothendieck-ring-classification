"""Exact finite group layer; does not identify a categorical dual tensor.

The four dimensional quadratic space is the orthogonal sum of two
anisotropic planes.  Thus q(x,y)=[x!=0]+[y!=0] mod 2.  This choice matters:
the electric Lagrangian is diagonal, and its stabilizer is the pointed
bimodule parabolic diag(S3) x C2, rather than an unnamed S3 x C2.
"""
from itertools import permutations, product
from collections import Counter
from pathlib import Path
import json

P=Path(__file__).resolve().parent
def need(v,msg):
    if not v: raise ValueError(msg)
S=[(0,)+p for p in permutations((1,2,3))]
si={a:i for i,a in enumerate(S)}
one=si[(0,1,2,3)]
def sm(a,b): return si[tuple(S[a][S[b][i]] for i in range(4))]
def sign(a): return sum(S[a][i]>S[a][j] for i in range(1,4) for j in range(i+1,4))%2
O=list(product(range(6),range(6),range(2)))
identity=(one,one,0)
def mul(x,y):
    a,b,e=x; c,d,f=y
    if e: c,d=d,c
    return sm(a,c),sm(b,d),e^f
def inv(x): return next(y for y in O if mul(x,y)==identity)
def act(g,v):
    a,b,e=g;x,y=v
    if e:x,y=y,x
    return S[a][x],S[b][y]
V=list(product(range(4),repeat=2))
def q(v): return int(v[0]!=0)^int(v[1]!=0)
L={(x,x) for x in range(4)}
parabolic={g for g in O if {act(g,v) for v in L}==L}
need(len(set(tuple(act(g,v) for v in V) for g in O))==72,'faithful action')
need(all(q(act(g,v))==q(v) for g in O for v in V),'quadratic form')
need(parabolic=={(a,a,e) for a in range(6) for e in range(2)},'pointed parabolic')
H={(a,a,0) for a in range(6)}
N={g for g in O if g[2]==0 and sign(g[0])==sign(g[1])==0}
need(len(N)==9,'normal C3 squared')
need([v for v in V if all(act(g,v)==v for g in N)]==[(0,0)],'N fixed vectors')
rows=[]
for ca,ce in [(0,1),(1,0),(1,1)]:
    U={g for g in O if (ca*(sign(g[0])+sign(g[1]))+ce*g[2])%2==0}
    need(len(U)==36 and all(mul(x,y) in U for x in U for y in U),'index two subgroup')
    need(N<=U and H<=U,'common subgroups')
    quotient={((sign(a),sign(b),e)) for a,b,e in U}
    def qm(x,y):
        a,b,e=x;c,d,f=y
        if e:c,d=d,c
        return a^c,b^d,e^f
    orders=[]
    for x in quotient:
        y=(0,0,0)
        for k in range(1,5):
            y=qm(y,x)
            if y==(0,0,0):orders.append(k);break
    doublecosets=[];left=set(U)
    while left:
        u=min(left);orbit={mul(mul(h,u),k) for h in H for k in H}
        doublecosets.append(len(orbit));left-=orbit
    component_ranks=Counter(len(L&{act(g,v)for v in L})for g in U)
    rows.append(dict(character=[ca,ce],size=len(U),pointed_grades=len(U&parabolic),component_rank_counts=dict(sorted(component_ranks.items())),
                     quotient_orders=sorted(orders),H_double_coset_sizes=sorted(doublecosets),
                     admissible=len(U&parabolic)==6))
need([r['admissible'] for r in rows]==[True,False,True],'two retained subgroups')
out=dict(scope='finite group and quadratic-space layer only',quadratic_space='anisotropic plane orthogonal sum anisotropic plane',
         group_order=72,pointed_parabolic_order=12,reverse_H_order=6,N_order=9,N_fixed_vectors=1,index_two_subgroups=rows,
         cohomology_argument='H^j(N,F2^4)=0 for j>0 by averaging, H^0=0 by exact fixed-vector check; LHS gives H^j(U,F2^4)=0 for all j>=0.',
         categorical_dual_tensor_identified=False)
(P/'brpic_replay.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

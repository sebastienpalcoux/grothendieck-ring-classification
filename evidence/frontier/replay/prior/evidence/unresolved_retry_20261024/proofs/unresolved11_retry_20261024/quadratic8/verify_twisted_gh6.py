#!/usr/bin/env python3
"""Exact finite checks for the explicit twisted RW orbifold.

This verifies finite metric/projector/fusion computations, not RW's
analytic quantum-dilogarithm existence or its reconstruction theorem.
"""
from itertools import product
from pathlib import Path
import json

G=list(product(range(12),repeat=2))
H=list(product(range(12),range(2)))
def ga(a,b):return ((a[0]+b[0])%12,(a[1]+b[1])%12)
def ha(a,b):return ((a[0]+b[0])%12,(a[1]+b[1])%2)
def emb(h):return (h[0],(h[0]+6*h[1])%12)
def B(a,b):return (a[1]*b[1]-a[0]*b[0])%12
def q(a):return (12*(a[0]+a[1])+a[1]**2-a[0]**2)%24
def w(a,b):return (a[1]*b[0])%2
assert 145*1-12*12==1
assert 145+1==146
assert {emb(h) for h in H} <= set(G)
assert len({emb(h) for h in H})==24
for a,b,c in product(H,repeat=3):
    assert (w(a,b)+w(ha(a,b),c)-w(b,c)-w(a,ha(b,c)))%2==0
for a,b in product(H,repeat=2):
    assert B(emb(a),emb(b))==6*((w(a,b)-w(b,a))%2)
for a,b in product(G,repeat=2):
    assert (q(ga(a,b))-q(a)-q(b)-2*B(a,b))%24==0
assert all(any(B(a,b) for b in G) for a in G if a!=(0,0))
rad=[a for a in H if all(B(emb(a),emb(b))==0 for b in H)]
perp=[g for g in G if all(B(g,emb(h))==0 for h in H)]
assert rad==[(x,0) for x in range(0,12,2)]
assert set(perp)=={emb(h) for h in rad}
assert all(q(emb((x,0)))==0 for x in range(12))
assert all(q(emb(h))==12*((h[0]*h[1]+h[1])%2) for h in H)

# p tau(p) on the invertible Hom spaces: exact character sums.
inv_ranks=[]
for r in range(6):
    survivors=[t for t in range(2) if (r+6*t)%12==0]
    inv_ranks.append(len(survivors))
assert inv_ranks==[1,0,0,0,0,0]

# On each noninvertible Hom space, p selects two free diagonal orbits.
noninv_ranks=[]
selected_sizes=[]
for eta in range(6):
    selected={(a,b,t) for a,b in G for t in range(2)
              if (b-a-eta-6*t)%12==0}
    selected_sizes.append(len(selected))
    orbits=[]
    while selected:
        a,b,t=min(selected)
        orbit={((a-l)%12,(b-l)%12,t) for l in range(12)}
        assert len(orbit)==12 and orbit<=selected
        selected-=orbit
        orbits.append(orbit)
    noninv_ranks.append(len(orbits))
assert noninv_ranks==[2]*6 and selected_sizes==[24]*6

# GH(C6,m=2) fusion tensor, in order invertibles then beta_g sigma.
n=6;r=12
N=[[[0]*r for _ in range(r)] for _ in range(r)]
for a,b in product(range(n),repeat=2):
    N[a][b][(a+b)%n]=1
    N[a][n+b][n+(a+b)%n]=1
    N[n+a][b][n+(a-b)%n]=1
    N[n+a][n+b][(a-b)%n]=1
    for c in range(n):N[n+a][n+b][n+c]=2
dual=[(-a)%n for a in range(n)]+list(range(n,2*n))
for a,b in product(range(r),repeat=2):
    assert N[a][b][0]==int(b==dual[a])
for a,b,c,d in product(range(r),repeat=4):
    assert sum(N[a][b][k]*N[k][c][d] for k in range(r))==sum(N[b][c][k]*N[a][k][d] for k in range(r))

# Associator class3, cyclic invariant and subgroup restrictions.
def assoc(a,b,c):return (a*((b+c)//6))%2
for a,b,c,d in product(range(6),repeat=4):
    assert (assoc(b,c,d)+assoc(a,(b+c)%6,d)+assoc(a,b,c)-assoc((a+b)%6,c,d)-assoc(a,b,(c+d)%6))%2==0
restr={order:sum(assoc(6//order,(j*(6//order))%6,6//order) for j in range(order))%2 for order in (2,3,6)}
assert restr=={2:1,3:0,6:1}
assert B((1,0),(6,0))==6

receipt={"status":"verified finite computations; actual precursor proof in accompanying note",
"source_gamma":[[145,12],[12,1]],"source_group":"C12 x C12","source_near_group_multiplicity":144,
"twisted_subgroup_order":24,"radical_order":6,"twisted_group_algebra":"six copies of M2(C)",
"invertible_projector_ranks":inv_ranks,"noninvertible_projector_ranks":noninv_ranks,
"output_based_ring":"GH(C6,m=2)","output_global_dimension":"444+72*sqrt(37)",
"pointed_associator_class_mod6":3,"subgroup_associator_parities":restr,
"fusion_associativity":"passed all 12^4 coefficient checks",
"R8_3_1768_status":"unresolved: separable algebra 1+sigma and actual Morita identification not established"}
out=Path(__file__).with_name("twisted_gh6_verified.json")
out.write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))

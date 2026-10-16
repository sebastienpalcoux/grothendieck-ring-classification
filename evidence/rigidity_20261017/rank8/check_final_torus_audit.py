"""Independent all-associator-slot arithmetic audit for the R24 torus proof.

This file verifies fusion combinatorics and integer lattice/phase claims only.
It does not certify the categorical normalization or the ENO application.
It intentionally does not import the pre-existing F-weight checker.
"""
from itertools import product
from pathlib import Path
import hashlib,json

# Literal fusion coefficients, ordered 1,g,r,s, with (s = gr).
N=[
 [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],
 [[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]],
 [[0,0,1,0],[0,0,0,1],[1,0,2,2],[0,1,2,2]],
 [[0,0,0,1],[0,0,1,0],[0,1,2,2],[1,0,2,2]],
]
bit=[0,1,0,1]
noninv=[0,0,1,1]

def require(ok,message):
    if not ok:raise RuntimeError(message)

def vertex(i,j,k,b):
    require(0<=b<N[i][j][k],'Invalid basis index')
    thick=N[i][j][k]==2
    require(thick==(noninv[i]+noninv[j]+noninv[k]==3),'Thick incidence discrepancy')
    tau=bit[i]^bit[j]^bit[k]
    if not thick:
        require(tau==0,'Nontrivial thin bit character')
        return (0,0,0,'thin')
    sign=1 if b==0 else -1
    return (sign,0,0,'H') if tau==0 else (0,sign,b,'J')

blocks=slots=phases=0
weights=set()
for a,b,c,d in product(range(4),repeat=4):
    lsize=sum(N[a][b][e]*N[e][c][d] for e in range(4))
    rsize=sum(N[b][c][f]*N[a][f][d] for f in range(4))
    require(lsize==rsize,'Associativity dimension mismatch')
    if lsize:blocks+=1
    counted=0
    for e,f in product(range(4),repeat=2):
        for i,j,k,l in product(range(N[a][b][e]),range(N[e][c][d]),range(N[b][c][f]),range(N[a][f][d])):
            vs=[vertex(a,b,e,i),vertex(e,c,d,j),vertex(b,c,f,k),vertex(a,f,d,l)]
            require(sum(v[3]=='H' for v in vs)%2==0,'Odd H incidence')
            require(sum(v[3]=='J' for v in vs)%2==0,'Odd J incidence')
            p=vs[0][0]+vs[1][0]-vs[2][0]-vs[3][0]
            q=vs[0][1]+vs[1][1]-vs[2][1]-vs[3][1]
            require(p%2==q%2==0 and abs(p)+abs(q)<=4,'Weight outside W')
            weights.add((p,q));counted+=1;slots+=1
            sign_parity=sum(v[2] for v in vs)%2
            for u_exponent in [1,3,5,7]:
                exponent=(u_exponent*p+4*sign_parity)%8
                require(exponent!=0 or p==0,'Reflection permits nonzero H weight')
                phases+=1
    require(counted==lsize*rsize,'Missing F coefficient slots')
W={(p,q) for p,q in product(range(-4,5,2),repeat=2) if abs(p)+abs(q)<=4}
require(weights==W,'Full possible weight set differs from W')
pairs=[]
for x,y in product(sorted(W),repeat=2):
    det=x[0]*y[1]-x[1]*y[0]
    if det==0:continue
    certificates=[]
    for target in [(4,0),(0,4)]:
        na=target[0]*y[1]-target[1]*y[0]
        nb=x[0]*target[1]-x[1]*target[0]
        require(na%det==0 and nb%det==0,'Fourth axis missing from pair lattice')
        aa,bb=na//det,nb//det
        require(tuple(aa*x[i]+bb*y[i] for i in range(2))==target,'Lattice witness invalid')
        certificates.append([aa,bb])
    pairs.append({'x':x,'y':y,'axis_coefficients':certificates})
source=Path(__file__).with_name('R24_TORUS_RIGIDITY_PROOF.md')
receipt={'status':'PASS','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'nonempty_blocks':blocks,'F_coefficient_slots':slots,'reflection_phase_checks':phases,'independent_pair_checks':len(pairs),'possible_weights':sorted(W),'categorical_claims_automatically_verified':False,'pair_witnesses':pairs}
print(json.dumps(receipt,indent=2))

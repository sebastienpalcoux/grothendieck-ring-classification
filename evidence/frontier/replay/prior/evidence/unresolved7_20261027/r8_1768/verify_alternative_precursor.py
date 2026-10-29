"""Short exact check of a second RW arithmetic input, not a model certificate."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

def need(v, message):
    if not v:
        raise ValueError(message)

n=12
elts=list(product(range(n),repeat=2))
def add(u,v): return tuple((x+y)%n for x,y in zip(u,v))
def mat(u,A): return ((u[0]*A[0][0]+u[1]*A[1][0])%n,(u[0]*A[0][1]+u[1]*A[1][1])%n)
def mul(A,B): return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def det(A): return A[0][0]*A[1][1]-A[0][1]*A[1][0]
A=[[7,12],[3,5]]
gamma=mul(A,A)
need(det(A)==-1 and gamma==[[85,144],[36,61]],'square')
need(gamma==[[1+12*A[0][0],12*A[0][1]],[12*A[1][0],1+12*A[1][1]]],'Pell')
need(det(gamma)==1 and gamma[0][0]+gamma[1][1]==146,'hyperbolic')
# Since A is unimodular, the row lattice of gamma-I is precisely 12 Z^2.
def be(u,v):
    x,y=u; a,b=v
    return (7*x*b+7*y*a+3*y*b)%12
def qe(u):
    x,y=u
    return (14*x*y+3*y*y+12*y)%24
def old_be(u,v): return (-u[0]*v[0]+u[1]*v[1])%12
def old_qe(u): return (12*(u[0]+u[1])+u[1]**2-u[0]**2)%24
M=[[2,5],[11,7]]  # row vectors: (x,y)M=(2x+11y,5x+7y)
need(len({mat(u,M) for u in elts})==144,'metric map bijective')
for u in elts:
    need(qe(mat(u,M))==old_qe(u),'quadratic metric isometry')
    for v in elts:
        need(be(u,v)==be(v,u),'symmetric')
        need((qe(add(u,v))-qe(u)-qe(v)-2*be(u,v))%24==0,'polarization')
        need(be(mat(u,M),mat(v,M))==old_be(u,v),'bicharacter isometry')
L=[(x,0) for x in range(12)]
H=[(x,6*t) for x in range(12) for t in range(2)]
K=[(2*x,0) for x in range(6)]
need([u for u in elts if all(be(u,l)==0 for l in L)]==L,'L Lagrangian')
need([u for u in elts if all(be(u,h)==0 for h in H)]==K,'H perp')
def oe(h,k): return ((h[1]//6)*k[0])%2
for h in H:
    x,t=h[0],h[1]//6
    need(qe(h)==12*((x*t+t)%2),'H quadratic restriction')
    for k in H:
        need(be(h,k)==6*((oe(h,k)-oe(k,h))%2),'twisted commutator')
        for z in H:
            need((oe(h,k)+oe(add(h,k),z)-oe(k,z)-oe(h,add(k,z)))%2==0,'2-cocycle')
need(all(qe(l)==0 for l in L),'isotropic q')
need(be((0,1),(0,6))==6,'cyclic associator anomaly')
need([mat(l,A) for l in L]==[((7*x)%12,0) for x in range(12)],'norm-minus-one action')
c,d=36,61
dedekind=sum((F(k,c)-F(1,2))*(F((d*k)%c,c)-F(1,2)) for k in range(1,c))
eta=F(146,12*c)-dedekind-F(1,4)
need(dedekind==F(19,216) and eta==0,'eta multiplier')
out={'result':'PASS','scope':'arithmetic and crossed-product input; no R1768 model certified',
     'A':A,'gamma':gamma,'group':'C12 x C12','eta_multiplier':1,
     'L_size':len(L),'H_size':len(H),'K_size':len(K),
     'quadratic_metric_isometry_row_matrix':M,'pointed_C6_class':3,
     'norm_minus_one_action_on_L':'x -> 7x modulo 12',
     'unproved':['equivalence or inequivalence to old precursor',
                 'connected separable algebra fixed by pointed involution',
                 'actual dual fusion ring equals R8_3_1768']}
Path(__file__).with_name('alternative_precursor_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: alternative RW input; no categorification of R1768 claimed')

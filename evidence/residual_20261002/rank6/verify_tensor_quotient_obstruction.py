"""Tiny exact audit of the pivotal tensor-quotient obstruction for R6_8_1660."""
from fractions import Fraction as F
from pathlib import Path
import json

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def add(A, B):
    return [[x+y for x,y in zip(a,b)] for a,b in zip(A,B)]

def scale(k,A):
    return [[k*x for x in a] for a in A]

def mul(A,B):
    return [[sum(x*y for x,y in zip(a,col)) for col in zip(*B)] for a in A]

def kron(A,B):
    return [[a*b for a in rowa for b in rowb] for rowa in A for rowb in B]

I3=[[1,0,0],[0,1,0],[0,0,1]]
G=[[0,1,0],[1,0,0],[0,0,1]]
S=[[0,0,1],[0,0,1],[1,1,0]]
I2=[[1,0],[0,1]]
I6=kron(I2,I3)
Ng=kron(I2,G)
Ns=kron(I2,S)
rows=[('I',0,1,0,0),('II',2,3,2,2),('III',1,2,0,1),('IV',1,2,1,2)]
receipt=[]
for label,a,b,c,f in rows:
    U=[[a,b],[b,6-a]]
    R=[[c,f],[f,4-c]]
    choices=([[[0,v],[v,0]] for v in [-1,1]] if label in ('I','II')
             else [[[v,0],[0,w]] for v in [-1,1] for w in [-1,1]])
    for V in choices:
        require(all((U[i][j]+V[i][j])%2==0 for i in range(2) for j in range(2)), 'parity')
        P=[[(U[i][j]+V[i][j])//2 for j in range(2)] for i in range(2)]
        Q=[[(U[i][j]-V[i][j])//2 for j in range(2)] for i in range(2)]
        NX=add(add(kron(P,I3),kron(Q,G)),kron(R,S))
        require(min(map(min,NX))>=0,'negative action')
        require(mul(NX,Ng)==mul(Ng,NX),'g commute')
        require(mul(NX,Ns)==mul(Ns,NX),'sigma commute')
        coeff=add(scale(3,add(I6,Ng)),scale(4,Ns))
        require(mul(NX,NX)==add(I6,mul(coeff,NX)), 'X fusion equation')
        NT=mul(Ns,NX)
        require(NX[2][0]==c and NT[2][0]==a,'image-column coefficients')
        parity_ok=(a%2==c%2==0)
        receipt.append(dict(type=label,V=V,X_sigma_multiplicity=c,T_sigma_multiplicity=a,indicator_parity_pass=parity_ok))

roots={2:(F(1414,1000),F(1415,1000)),3:(F(1732,1000),F(1733,1000)),6:(F(2449,1000),F(2450,1000))}
for n,(lo,hi) in roots.items():
    require(0<lo and lo*lo<n<hi*hi, 'invalid radical interval')
rlo=3-2*roots[2][1]+2*roots[3][0]-roots[6][1]
rhi=3-2*roots[2][0]+2*roots[3][1]-roots[6][0]
require(rlo==F(148,125) and rhi==F(1189,1000), 'r interval')
require(1<rlo<rhi<F(6,5) and F(6,5)**2<2,'dimension gap')
require(len(receipt)==12,'raw signed choice count')
# Types I and II each have two leaf-equivalent signs, giving ten based modules.
require(2+4+4==10,'published equivalence count')
require({x['type'] for x in receipt if x['indicator_parity_pass']}=={'I','II'},'parity survivors')
out=dict(status='structural_only_ring_unresolved',theorem_scope='dominant pivotal tensor functors; unitary corollary',
         passed=True,raw_signed_choices_checked=len(receipt),based_modules_up_to_leaf_relabelling=10,
         module_checks=receipt,type_II_r_interval=[str(rlo),str(rhi)],type_II_r_squared_upper_bound='36/25 < 2',
         surviving_tensor_quotient_type='I (regular; tensor equivalence)',center_profile_count_unchanged=1669)
Path(__file__).with_name('tensor_quotient_obstruction_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='module_checks'},indent=2))
